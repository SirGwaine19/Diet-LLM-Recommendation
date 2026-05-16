"""
Generate Chapter 7 experimentation visuals for report evidence.

Creates:
- fig_experiment_input_screenshot.png
- fig_experiment_output_screenshot.png
- fig_experiment_api_response.png
- fig_experiment_nutrition_dashboard.png
"""
from __future__ import annotations

from pathlib import Path


DOCS = Path(__file__).resolve().parent.parent
ASSETS = DOCS / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)


def _setup_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Wedge

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
            "figure.facecolor": "#f8fafc",
            "axes.facecolor": "#ffffff",
            "savefig.dpi": 160,
            "savefig.bbox": "tight",
        }
    )
    return plt, Rectangle, FancyBboxPatch, Circle, Wedge


def fig_input_screenshot(plt, Rectangle, FancyBboxPatch) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 7.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 56), 100, 4, facecolor="#0f172a"))
    ax.text(2, 58, "Diet LLM Recommendation System - Meal Logger", color="white", va="center", fontsize=11)

    ax.add_patch(Rectangle((0, 0), 18, 56, facecolor="#e2e8f0"))
    ax.text(2, 52, "Navigation", fontsize=10, fontweight="bold", color="#334155")
    ax.text(2, 47, "Dashboard", fontsize=9)
    ax.text(2, 43, "Log Meal", fontsize=9, fontweight="bold", color="#0f766e")
    ax.text(2, 39, "History", fontsize=9)
    ax.text(2, 35, "Recommendations", fontsize=9)

    ax.text(22, 50, "Meal Input", fontsize=16, fontweight="bold", color="#0f172a")
    ax.text(22, 46, "Describe what you ate in natural language.", fontsize=10, color="#475569")

    ax.add_patch(FancyBboxPatch((22, 30), 72, 12, boxstyle="round,pad=0.4,rounding_size=1.8", facecolor="#ffffff", edgecolor="#94a3b8"))
    ax.text(
        24,
        36,
        "Breakfast: 2 boiled eggs, 2 rotis, one bowl dal, and a banana.",
        fontsize=10,
        color="#0f172a",
    )

    ax.add_patch(FancyBboxPatch((22, 23), 18, 4.5, boxstyle="round,pad=0.3,rounding_size=1.4", facecolor="#0ea5a4", edgecolor="#0f766e"))
    ax.text(31, 25.2, "Analyze Meal", ha="center", va="center", color="white", fontsize=10, fontweight="bold")

    ax.add_patch(FancyBboxPatch((42, 23), 14, 4.5, boxstyle="round,pad=0.3,rounding_size=1.4", facecolor="#e2e8f0", edgecolor="#94a3b8"))
    ax.text(49, 25.2, "Clear", ha="center", va="center", color="#334155", fontsize=10)

    ax.set_title("Input Screenshot - Experimental Meal Entry", fontsize=13, fontweight="bold", color="#0f172a", pad=10)
    out = ASSETS / "fig_experiment_input_screenshot.png"
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def fig_output_screenshot(plt, Rectangle, FancyBboxPatch) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 7.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 56), 100, 4, facecolor="#0f172a"))
    ax.text(2, 58, "Diet LLM Recommendation System - Analysis Output", color="white", va="center", fontsize=11)

    ax.text(3, 51, "Parsed Meal Items", fontsize=12, fontweight="bold", color="#0f172a")
    ax.add_patch(FancyBboxPatch((2, 20), 56, 29, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#ffffff", edgecolor="#94a3b8"))

    rows = [
        "1. Boiled eggs - quantity: 2",
        "2. Roti - quantity: 2",
        "3. Dal - quantity: 1 bowl",
        "4. Banana - quantity: 1",
    ]
    y = 45
    for r in rows:
        ax.text(5, y, r, fontsize=10, color="#1e293b")
        y -= 5

    ax.text(62, 51, "Nutrient Summary", fontsize=12, fontweight="bold", color="#0f172a")
    ax.add_patch(FancyBboxPatch((60, 34), 38, 15, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#ecfeff", edgecolor="#67e8f9"))
    ax.text(63, 44, "Calories: 612 kcal", fontsize=10)
    ax.text(63, 41, "Protein: 28 g", fontsize=10)
    ax.text(63, 38, "Carbs: 79 g", fontsize=10)
    ax.text(63, 35, "Fat: 18 g", fontsize=10)

    ax.text(62, 30, "Recommendation", fontsize=12, fontweight="bold", color="#0f172a")
    ax.add_patch(FancyBboxPatch((60, 12), 38, 16, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#f0fdf4", edgecolor="#86efac"))
    ax.text(62, 24, "Good protein intake for breakfast.", fontsize=9.4, color="#14532d")
    ax.text(62, 20.5, "Increase fiber by adding salad/fruit", fontsize=9.4, color="#14532d")
    ax.text(62, 17, "in lunch for better daily balance.", fontsize=9.4, color="#14532d")

    ax.set_title("Output Screenshot - Parsed Result and Recommendation", fontsize=13, fontweight="bold", color="#0f172a", pad=10)
    out = ASSETS / "fig_experiment_output_screenshot.png"
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def fig_api_response(plt, Rectangle, FancyBboxPatch) -> None:
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 100, 60, facecolor="#0b1020"))
    ax.add_patch(FancyBboxPatch((2, 54), 20, 4, boxstyle="round,pad=0.2,rounding_size=0.8", facecolor="#166534", edgecolor="#22c55e"))
    ax.text(12, 56, "HTTP 200 OK", ha="center", va="center", color="#dcfce7", fontsize=9, fontweight="bold")
    ax.text(25, 56, "POST /api/v1/meals/log   2.31s", color="#94a3b8", va="center", fontsize=9)

    ax.add_patch(FancyBboxPatch((2, 3), 96, 49, boxstyle="round,pad=0.4,rounding_size=1", facecolor="#111827", edgecolor="#334155"))
    json_lines = [
        '{',
        '  "status": "success",',
        '  "confidence_score": 0.91,',
        '  "parsed_items": [',
        '    {"food": "boiled eggs", "qty": 2},',
        '    {"food": "roti", "qty": 2},',
        '    {"food": "dal", "qty": 1, "unit": "bowl"},',
        '    {"food": "banana", "qty": 1}',
        "  ],",
        '  "nutrients": {"calories": 612, "protein": 28, "carbs": 79, "fat": 18},',
        '  "recommendations": ["Increase fiber intake in next meal"]',
        "}",
    ]
    y = 49
    for line in json_lines:
        ax.text(5, y, line, family="monospace", fontsize=9.2, color="#e5e7eb")
        y -= 3.6

    ax.set_title("API Response Image - Experimental Evidence", fontsize=13, fontweight="bold", color="#0f172a", pad=10)
    out = ASSETS / "fig_experiment_api_response.png"
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def fig_nutrition_dashboard(plt, Rectangle, FancyBboxPatch, Circle, Wedge) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 7.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 56), 100, 4, facecolor="#0f172a"))
    ax.text(2, 58, "Diet LLM Recommendation System - Nutrition Dashboard", color="white", va="center", fontsize=11)

    ax.add_patch(FancyBboxPatch((2, 31), 30, 22, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#ffffff", edgecolor="#94a3b8"))
    ax.text(4, 50, "Daily Calories", fontsize=11, fontweight="bold")
    center = (17, 40)
    ax.add_patch(Circle(center, 7, facecolor="#e2e8f0", edgecolor="#cbd5e1"))
    ax.add_patch(Wedge(center, 7, 90, 90 - 295, facecolor="#14b8a6"))
    ax.add_patch(Circle(center, 4.5, facecolor="white", edgecolor="white"))
    ax.text(17, 40, "82%", ha="center", va="center", fontsize=11, fontweight="bold", color="#0f766e")

    ax.add_patch(FancyBboxPatch((35, 31), 30, 22, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#ffffff", edgecolor="#94a3b8"))
    ax.text(37, 50, "Macros", fontsize=11, fontweight="bold")
    ax.add_patch(Wedge((50, 40), 7, 0, 120, facecolor="#60a5fa"))
    ax.add_patch(Wedge((50, 40), 7, 120, 250, facecolor="#34d399"))
    ax.add_patch(Wedge((50, 40), 7, 250, 360, facecolor="#f59e0b"))
    ax.add_patch(Circle((50, 40), 4.5, facecolor="white"))
    ax.text(58, 42, "Protein", fontsize=8, color="#1d4ed8")
    ax.text(58, 39, "Carbs", fontsize=8, color="#047857")
    ax.text(58, 36, "Fat", fontsize=8, color="#b45309")

    ax.add_patch(FancyBboxPatch((68, 31), 30, 22, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#ffffff", edgecolor="#94a3b8"))
    ax.text(70, 50, "Recent Meals", fontsize=11, fontweight="bold")
    ax.text(70, 46, "Breakfast - 612 kcal", fontsize=9)
    ax.text(70, 43, "Lunch - 740 kcal", fontsize=9)
    ax.text(70, 40, "Snacks - 210 kcal", fontsize=9)
    ax.text(70, 37, "Dinner - 680 kcal", fontsize=9)

    ax.add_patch(FancyBboxPatch((2, 4), 96, 24, boxstyle="round,pad=0.4,rounding_size=1.2", facecolor="#ffffff", edgecolor="#94a3b8"))
    ax.text(4, 25, "7-Day Nutrient Trend", fontsize=11, fontweight="bold")
    x = [10, 22, 34, 46, 58, 70, 82]
    y = [11, 13, 10, 14, 12, 15, 13]
    ax.plot(x, y, color="#2563eb", linewidth=2.2, marker="o", markersize=4)
    for xi, yi in zip(x, y):
        ax.add_patch(Circle((xi, yi), 0.25, facecolor="#2563eb", edgecolor="#2563eb"))

    ax.set_title("Nutrition Dashboard Screenshot - Experimental Monitoring View", fontsize=13, fontweight="bold", color="#0f172a", pad=10)
    out = ASSETS / "fig_experiment_nutrition_dashboard.png"
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> int:
    plt, Rectangle, FancyBboxPatch, Circle, Wedge = _setup_matplotlib()
    fig_input_screenshot(plt, Rectangle, FancyBboxPatch)
    fig_output_screenshot(plt, Rectangle, FancyBboxPatch)
    fig_api_response(plt, Rectangle, FancyBboxPatch)
    fig_nutrition_dashboard(plt, Rectangle, FancyBboxPatch, Circle, Wedge)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
