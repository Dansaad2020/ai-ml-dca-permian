from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFont


# This is the normalized Martin County production file packaged with this repository.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "martin_selected_30_monthly_production_normalized.csv"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "dca_outputs"
FIT_START_MONTH = 2
FIT_END_MONTH = 24
TEST_START_MONTH = 25
TEST_END_MONTH = 33


def resolve_data_file() -> Path:
    """Use the repository-packaged processed cohort."""
    if DATA_FILE.exists():
        return DATA_FILE
    raise FileNotFoundError(f"Could not find {DATA_FILE}")


def to_float(value: str) -> float | None:
    """Convert CSV text to float while tolerating blanks and malformed values."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_data() -> list[dict[str, object]]:
    """Load production data using only the standard library."""
    rows: list[dict[str, object]] = []
    with resolve_data_file().open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            month = to_float(row.get("month_on_production", ""))
            oil = to_float(row.get("oil_bbl", ""))
            if month is None or oil is None:
                continue

            rows.append(
                {
                    "api8": row.get("api8", ""),
                    "month_on_production": int(month),
                    "oil_bbl": oil,
                }
            )

    return sorted(rows, key=lambda item: (str(item["api8"]), int(item["month_on_production"])))


def build_median_curve(rows: list[dict[str, object]]) -> list[dict[str, float]]:
    """Create a median oil type curve for the full-cohort window, months 1-33."""
    by_month: dict[int, list[float]] = {}
    for row in rows:
        month = int(row["month_on_production"])
        if 1 <= month <= TEST_END_MONTH:
            by_month.setdefault(month, []).append(float(row["oil_bbl"]))

    return [
        {
            "month_on_production": float(month),
            "median_oil_bbl": float(median(values)),
        }
        for month, values in sorted(by_month.items())
    ]


def predict_hyperbolic(month: float, qi: float, di: float, b_factor: float) -> float:
    """Predict q(t) = qi / (1 + b * Di * t)^(1 / b)."""
    return qi / ((1.0 + b_factor * di * month) ** (1.0 / b_factor))


def log_space_sse(
    fit_points: list[dict[str, float]], di: float, b_factor: float
) -> tuple[float, float]:
    """Return log-space SSE and optimal qi for fixed Di and b."""
    adjusted_logs = []
    for point in fit_points:
        month = point["month_on_production"]
        rate = point["median_oil_bbl"]
        adjusted_logs.append(math.log(rate) + (1.0 / b_factor) * math.log1p(b_factor * di * month))

    log_qi = sum(adjusted_logs) / len(adjusted_logs)
    qi = math.exp(log_qi)

    sse = 0.0
    for point in fit_points:
        actual_log = math.log(point["median_oil_bbl"])
        predicted_log = math.log(predict_hyperbolic(point["month_on_production"], qi, di, b_factor))
        sse += (actual_log - predicted_log) ** 2

    return sse, qi


def fit_hyperbolic_decline(
    curve: list[dict[str, float]],
    start_month: int = FIT_START_MONTH,
    end_month: int = FIT_END_MONTH,
) -> tuple[float, float, float, list[dict[str, float]]]:
    """Fit hyperbolic decline with a dependency-free bounded search."""
    fit_points = [
        point
        for point in curve
        if start_month <= point["month_on_production"] <= end_month
        and point["median_oil_bbl"] > 0
    ]
    if len(fit_points) < 3:
        raise ValueError("At least three positive fit points are required.")

    best: tuple[float, float, float, float] | None = None

    # First pass: broad grid over common shale-style b and monthly Di ranges.
    for b_index in range(1, 151):
        b_factor = b_index / 100.0
        for di_index in range(1, 401):
            di = di_index / 1000.0
            sse, qi = log_space_sse(fit_points, di, b_factor)
            if best is None or sse < best[0]:
                best = (sse, qi, di, b_factor)

    assert best is not None
    _, _, best_di, best_b = best

    # Second pass: local refinement around the best broad-grid point.
    b_min = max(0.01, best_b - 0.02)
    b_max = min(1.50, best_b + 0.02)
    di_min = max(0.001, best_di - 0.01)
    di_max = min(0.400, best_di + 0.01)

    for b_step in range(81):
        b_factor = b_min + (b_max - b_min) * b_step / 80.0
        for di_step in range(101):
            di = di_min + (di_max - di_min) * di_step / 100.0
            sse, qi = log_space_sse(fit_points, di, b_factor)
            if sse < best[0]:
                best = (sse, qi, di, b_factor)

    _, qi, di, b_factor = best
    return qi, di, b_factor, fit_points


def metric_summary(curve: list[dict[str, float]], prediction_column: str) -> list[dict[str, float | str]]:
    """Compute train and test error metrics for the fitted median curve."""
    windows = [
        ("train", FIT_START_MONTH, FIT_END_MONTH),
        ("test", TEST_START_MONTH, TEST_END_MONTH),
    ]
    summaries: list[dict[str, float | str]] = []

    for window_name, start_month, end_month in windows:
        points = [
            point
            for point in curve
            if start_month <= point["month_on_production"] <= end_month
            and point["median_oil_bbl"] > 0
        ]
        errors = [point[prediction_column] - point["median_oil_bbl"] for point in points]
        abs_errors = [abs(error) for error in errors]
        squared_errors = [error**2 for error in errors]
        smape_terms = [
            abs(point[prediction_column] - point["median_oil_bbl"])
            / ((abs(point["median_oil_bbl"]) + abs(point[prediction_column])) / 2.0)
            for point in points
            if point["median_oil_bbl"] or point[prediction_column]
        ]

        summaries.append(
            {
                "model": "hyperbolic_decline",
                "window": window_name,
                "start_month": start_month,
                "end_month": end_month,
                "observations": len(points),
                "mae_bbl": sum(abs_errors) / len(abs_errors),
                "rmse_bbl": math.sqrt(sum(squared_errors) / len(squared_errors)),
                "bias_bbl": sum(errors) / len(errors),
                "smape_percent": 100.0 * sum(smape_terms) / len(smape_terms),
            }
        )

    return summaries


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write dictionaries to CSV."""
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def draw_plot(curve: list[dict[str, float]], path: Path) -> None:
    """Save a simple PNG plot without requiring matplotlib."""
    width, height = 1200, 720
    margin_left, margin_right = 95, 35
    margin_top, margin_bottom = 70, 80
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    x_values = [point["month_on_production"] for point in curve]
    y_values = [
        value
        for point in curve
        for value in (point["median_oil_bbl"], point["hyperbolic_fit_oil_bbl"])
    ]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = 0.0, max(y_values) * 1.08

    def x_coord(value: float) -> float:
        return margin_left + (value - x_min) / (x_max - x_min) * plot_width

    def y_coord(value: float) -> float:
        return margin_top + (y_max - value) / (y_max - y_min) * plot_height

    train_x0 = x_coord(FIT_START_MONTH)
    train_x1 = x_coord(FIT_END_MONTH)
    test_x0 = x_coord(TEST_START_MONTH)
    test_x1 = x_coord(TEST_END_MONTH)
    draw.rectangle((train_x0, margin_top, train_x1, height - margin_bottom), fill=(237, 247, 255))
    draw.rectangle((test_x0, margin_top, test_x1, height - margin_bottom), fill=(255, 246, 230))

    axis_color = (70, 70, 70)
    grid_color = (225, 225, 225)
    draw.line((margin_left, margin_top, margin_left, height - margin_bottom), fill=axis_color, width=2)
    draw.line((margin_left, height - margin_bottom, width - margin_right, height - margin_bottom), fill=axis_color, width=2)

    for month in range(1, TEST_END_MONTH + 1, 4):
        x = x_coord(float(month))
        draw.line((x, margin_top, x, height - margin_bottom), fill=grid_color)
        draw.text((x - 8, height - margin_bottom + 12), str(month), fill=axis_color, font=font)

    y_tick = 0
    while y_tick <= y_max:
        y = y_coord(float(y_tick))
        draw.line((margin_left, y, width - margin_right, y), fill=grid_color)
        draw.text((15, y - 6), f"{y_tick:,.0f}", fill=axis_color, font=font)
        y_tick += 5000

    actual_points = [(x_coord(point["month_on_production"]), y_coord(point["median_oil_bbl"])) for point in curve]
    fit_points = [(x_coord(point["month_on_production"]), y_coord(point["hyperbolic_fit_oil_bbl"])) for point in curve]

    draw.line(actual_points, fill=(31, 95, 151), width=3)
    draw.line(fit_points, fill=(205, 92, 92), width=3)

    for x, y in actual_points:
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(31, 95, 151))

    title = "Median Type Curve: Actual vs Hyperbolic Decline"
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) / 2, 30), title, fill=(30, 30, 30), font=font)
    draw.text((margin_left, height - 35), "Month on Production", fill=axis_color, font=font)
    draw.text((15, 12), "Oil Production (bbl/month)", fill=axis_color, font=font)

    legend_x = width - 310
    draw.line((legend_x, 40, legend_x + 45, 40), fill=(31, 95, 151), width=3)
    draw.text((legend_x + 55, 34), "Actual median oil", fill=axis_color, font=font)
    draw.line((legend_x, 62, legend_x + 45, 62), fill=(205, 92, 92), width=3)
    draw.text((legend_x + 55, 56), "Hyperbolic fit", fill=axis_color, font=font)

    image.save(path)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    rows = load_data()
    curve = build_median_curve(rows)
    qi, di, b_factor, fit_points = fit_hyperbolic_decline(curve)

    for point in curve:
        point["hyperbolic_fit_oil_bbl"] = predict_hyperbolic(
            point["month_on_production"], qi, di, b_factor
        )

    fit_summary = [
        {
            "curve_name": "median_type_curve",
            "fit_start_month": FIT_START_MONTH,
            "fit_end_month": FIT_END_MONTH,
            "qi_bbl_per_month": qi,
            "di_per_month": di,
            "di_percent_per_month": di * 100.0,
            "b_factor": b_factor,
        }
    ]
    metrics = metric_summary(curve, "hyperbolic_fit_oil_bbl")

    write_csv(OUTPUT_DIR / "median_hyperbolic_decline_curve.csv", curve)
    write_csv(OUTPUT_DIR / "hyperbolic_decline_fit_summary.csv", fit_summary)
    write_csv(OUTPUT_DIR / "hyperbolic_decline_metrics.csv", metrics)
    draw_plot(curve, OUTPUT_DIR / "median_hyperbolic_decline_fit.png")

    print("\n=== Hyperbolic Decline Fit: Median Type Curve ===")
    print(f"Fit months used: {int(fit_points[0]['month_on_production'])}-"
          f"{int(fit_points[-1]['month_on_production'])}")
    print(f"Fitted qi: {qi:,.0f} bbl/month")
    print(f"Fitted Di: {di:.4f} per month")
    print(f"Fitted Di: {di * 100:.2f}% per month")
    print(f"Fitted b-factor: {b_factor:.3f}")

    print("\n=== Saved Outputs ===")
    print(OUTPUT_DIR / "median_hyperbolic_decline_fit.png")
    print(OUTPUT_DIR / "median_hyperbolic_decline_curve.csv")
    print(OUTPUT_DIR / "hyperbolic_decline_fit_summary.csv")
    print(OUTPUT_DIR / "hyperbolic_decline_metrics.csv")

    print("\n=== Error Metrics ===")
    for row in metrics:
        print(
            f"{row['window']}: MAE={row['mae_bbl']:,.0f} bbl, "
            f"RMSE={row['rmse_bbl']:,.0f} bbl, "
            f"Bias={row['bias_bbl']:,.0f} bbl, "
            f"sMAPE={row['smape_percent']:.2f}%"
        )


if __name__ == "__main__":
    main()
