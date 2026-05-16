"""
Generate report figures: test-case summary table image and confusion matrices.

Uses illustrative counts aligned with docs/PROJECT_TABLES.md (Table 8–9, Table 16).
Requires: pip install matplotlib

Run from repo root:
  python docs/scripts/generate_test_figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Repo root = parent of docs/
DOCS = Path(__file__).resolve().parent.parent
ASSETS = DOCS / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)


def _setup_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial", "Helvetica"],
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "figure.facecolor": "#fafafa",
            "axes.facecolor": "#ffffff",
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
        }
    )
    return plt


def fig_test_cases_table(plt) -> None:
    """Table 16: Test Cases Summary as a figure."""
    rows = [
        ("TC-01", "Auth", "Registration with valid credentials", "Success, returns JWT"),
        ("TC-02", "Auth", "Registration with duplicate email", "400 Error"),
        ("TC-03", "Auth", "Login with correct credentials", "Success, returns JWT"),
        ("TC-04", "Auth", "Login with incorrect password", "401 Error"),
        ("TC-05", "Auth", "Access protected endpoint with valid JWT", "Success"),
        ("TC-06", "Auth", "Access with expired token", "401 Error"),
        ("TC-07", "Meal", 'Parse simple meal ("2 eggs and toast")', "Correct JSON extraction"),
        ("TC-08", "Meal", "Parse complex meal (multiple items)", "All items extracted"),
        ("TC-09", "Meal", 'Handle ambiguous quantities ("some salad")', "Default quantity applied"),
        ("TC-10", "Meal", "Match foods to database", "Correct matches"),
        ("TC-11", "Meal", "Calculate nutrients", "Accurate values"),
        ("TC-12", "Meal", "Store with timestamp", "Correct timestamp"),
        ("TC-13", "Rec", "Generate summary with meals", "Valid summary"),
        ("TC-14", "Rec", "Handle no meals logged", "Appropriate message"),
        ("TC-15", "Rec", "Personalized suggestions", "Based on goals"),
        ("TC-16", "Rec", "Non-judgmental tone", "Positive language"),
    ]

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.axis("off")
    fig.patch.set_facecolor("#f5f5f5")

    col_labels = ["ID", "Category", "Test case", "Expected result"]
    table_data = [[r[0], r[1], r[2], r[3]] for r in rows]

    table = ax.table(
        cellText=table_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="left",
        colColours=["#1a535c"] * 4,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.05, 2.0)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color="white", fontweight="bold")
            cell.set_height(0.045)
        else:
            cell.set_facecolor("#ffffff" if row % 2 else "#eef8f7")
            cell.set_edgecolor("#cccccc")
        cell.set_linewidth(0.5)

    fig.suptitle(
        "Table 16 — Test Cases Summary (Experimentation)",
        fontsize=15,
        fontweight="bold",
        color="#1a535c",
        y=0.98,
    )
    out = ASSETS / "fig_test_cases_summary.png"
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def fig_confusion_matrix(plt) -> None:
    """
    Confusion matrix for food-database matching (illustrative evaluation).

    Rows: ground-truth label. Columns: system prediction.
    Classes: Exact match | Partial match | No match
    """
    import numpy as np

    labels = ["Exact match", "Partial match", "No match"]
    # Illustrative counts (sum of diagonal ≈ agreement; off-diagonal = confusion)
    cm = np.array(
        [
            [142, 18, 7],
            [22, 58, 14],
            [8, 12, 31],
        ],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(8.2, 6.8))
    im = ax.imshow(cm, cmap="Blues", aspect="equal", vmin=0)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted label", fontweight="bold")
    ax.set_ylabel("Ground truth label", fontweight="bold")
    ax.set_title(
        "Confusion matrix — Food name matching (nutrition DB)\n"
        "(Illustrative counts for project report; align with Table 9)",
        fontsize=12,
        pad=12,
    )

    # Annotate cells
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = int(cm[i, j])
            color = "white" if cm[i, j] > cm.max() / 2 else "#1a1a1a"
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=13, fontweight="bold")

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Count")
    plt.tight_layout()
    out = ASSETS / "fig_confusion_matrix_food_matching.png"
    fig.savefig(out, facecolor="#fafafa")
    plt.close(fig)
    print(f"Wrote {out}")


def fig_confusion_matrix_llm_items(plt) -> None:
    """Second matrix: per-item extraction correctness (3-class)."""
    import numpy as np

    labels = ["Correct", "Partial", "Missed"]
    cm = np.array(
        [
            [185, 24, 11],
            [19, 47, 8],
            [14, 9, 23],
        ],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(8.2, 6.8))
    im = ax.imshow(cm, cmap="Greens", aspect="equal", vmin=0)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted (LLM + pipeline)", fontweight="bold")
    ax.set_ylabel("Ground truth (annotated)", fontweight="bold")
    ax.set_title(
        "Confusion matrix — Meal item extraction vs ground truth\n"
        "(Illustrative; relate to Table 8 F1 / precision / recall)",
        fontsize=12,
        pad=12,
    )

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = int(cm[i, j])
            color = "white" if cm[i, j] > cm.max() / 2 else "#1a1a1a"
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=13, fontweight="bold")

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Count")
    plt.tight_layout()
    out = ASSETS / "fig_confusion_matrix_llm_extraction.png"
    fig.savefig(out, facecolor="#fafafa")
    plt.close(fig)
    print(f"Wrote {out}")


def fig_accuracy_graph(plt) -> None:
    """Bar chart for parsing accuracy metrics."""
    metrics = ["Precision", "Recall", "F1 Score", "Qty Accuracy"]
    values = [92.3, 89.7, 91.0, 85.2]
    colors = ["#2a9d8f", "#2a9d8f", "#2a9d8f", "#e76f51"]

    fig, ax = plt.subplots(figsize=(9, 5.8))
    bars = ax.bar(metrics, values, color=colors, edgecolor="#1f1f1f", linewidth=0.6)
    ax.set_ylim(70, 100)
    ax.set_ylabel("Percentage (%)", fontweight="bold")
    ax.set_title("Accuracy Graph — Parsing Metrics", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.4,
            f"{val:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    plt.tight_layout()
    out = ASSETS / "fig_accuracy_graph.png"
    fig.savefig(out, facecolor="#fafafa")
    plt.close(fig)
    print(f"Wrote {out}")


def fig_latency_graph(plt) -> None:
    """Horizontal bar chart for endpoint latency."""
    endpoints = [
        "POST /auth/login",
        "GET /meals",
        "GET /recommendations/daily",
        "POST /meals/log",
        "POST /recommendations/generate",
    ]
    latency_ms = [120, 85, 180, 2300, 4100]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(endpoints, latency_ms, color="#457b9d", edgecolor="#1f1f1f", linewidth=0.6)
    ax.set_xlabel("Latency (ms)", fontweight="bold")
    ax.set_title("Latency Graph — API Performance", fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    for bar, val in zip(bars, latency_ms):
        ax.text(
            val + (80 if val < 1000 else 120),
            bar.get_y() + bar.get_height() / 2,
            f"{val} ms",
            va="center",
            fontsize=9,
        )

    plt.tight_layout()
    out = ASSETS / "fig_latency_graph.png"
    fig.savefig(out, facecolor="#fafafa")
    plt.close(fig)
    print(f"Wrote {out}")


def fig_user_satisfaction_graph(plt) -> None:
    """Line chart for user response factors."""
    categories = ["Ease of Logging", "Clarity", "Trust", "Overall Satisfaction"]
    scores = [4.5, 4.2, 4.1, 4.4]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(categories, scores, marker="o", color="#6a4c93", linewidth=2.2, markersize=7)
    ax.fill_between(categories, scores, [4.0] * len(scores), color="#cdb4db", alpha=0.3)
    ax.set_ylim(3.8, 5.0)
    ax.set_ylabel("Score (out of 5)", fontweight="bold")
    ax.set_title("User Satisfaction Graph", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for i, val in enumerate(scores):
        ax.text(i, val + 0.03, f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    out = ASSETS / "fig_user_satisfaction_graph.png"
    fig.savefig(out, facecolor="#fafafa")
    plt.close(fig)
    print(f"Wrote {out}")


def fig_nutrient_tracking_graph(plt) -> None:
    """Multi-line graph for 7-day nutrient tracking."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calories = [1980, 2050, 1925, 2100, 2020, 2160, 1995]
    protein = [72, 76, 70, 78, 75, 80, 74]
    carbs = [245, 258, 238, 265, 250, 272, 246]

    fig, ax1 = plt.subplots(figsize=(10.5, 6.2))
    ax1.plot(days, calories, marker="o", color="#e63946", linewidth=2.1, label="Calories (kcal)")
    ax1.set_ylabel("Calories (kcal)", color="#e63946", fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#e63946")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(days, protein, marker="s", color="#2a9d8f", linewidth=1.9, label="Protein (g)")
    ax2.plot(days, carbs, marker="^", color="#1d3557", linewidth=1.9, label="Carbs (g)")
    ax2.set_ylabel("Protein / Carbs (g)", color="#1d3557", fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#1d3557")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax1.set_title("Nutrient Tracking Graph — 7-Day Trend", fontweight="bold")

    plt.tight_layout()
    out = ASSETS / "fig_nutrient_tracking_graph.png"
    fig.savefig(out, facecolor="#fafafa")
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> int:
    try:
        plt = _setup_matplotlib()
    except ImportError:
        print("Install matplotlib: pip install matplotlib", file=sys.stderr)
        return 1

    fig_test_cases_table(plt)
    fig_confusion_matrix(plt)
    fig_confusion_matrix_llm_items(plt)
    fig_accuracy_graph(plt)
    fig_latency_graph(plt)
    fig_user_satisfaction_graph(plt)
    fig_nutrient_tracking_graph(plt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
