"""Reproducible analysis for the Indonesia e-commerce portfolio project."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecommerce_orders.csv"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

def rupiah_axis(ax):
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp{x/1e6:.0f}M"))

def main():
    df = pd.read_csv(DATA, parse_dates=["order_date"])
    # Basic data quality checks
    assert df["order_id"].is_unique, "Duplicate order IDs found"
    assert df[["revenue_idr", "estimated_cost_idr", "profit_idr"]].notna().all().all()
    assert (df["quantity"] > 0).all()
    assert (df["revenue_idr"] >= 0).all()

    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month", as_index=False).agg(
        orders=("order_id", "nunique"),
        revenue_idr=("revenue_idr", "sum"),
        profit_idr=("profit_idr", "sum"),
    )
    category = df.groupby("category", as_index=False).agg(
        orders=("order_id", "nunique"),
        revenue_idr=("revenue_idr", "sum"),
        profit_idr=("profit_idr", "sum"),
    ).sort_values("revenue_idr", ascending=False)
    city = df.groupby("city", as_index=False).agg(
        orders=("order_id", "nunique"),
        revenue_idr=("revenue_idr", "sum"),
        profit_idr=("profit_idr", "sum"),
    ).sort_values("revenue_idr", ascending=False)

    monthly.to_csv(OUT / "monthly_kpis.csv", index=False)
    category.to_csv(OUT / "category_performance.csv", index=False)
    city.to_csv(OUT / "city_performance.csv", index=False)

    # Chart 1: monthly revenue
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["month"], monthly["revenue_idr"], marker="o")
    ax.set(title="Monthly Revenue Trend (2025)", xlabel="Month", ylabel="Revenue (IDR)")
    ax.tick_params(axis="x", rotation=45)
    rupiah_axis(ax); ax.grid(alpha=.25); fig.tight_layout()
    fig.savefig(CHARTS / "monthly_revenue.png", dpi=160); plt.close(fig)

    # Chart 2: category revenue
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(category["category"], category["revenue_idr"])
    ax.set(title="Revenue by Product Category", xlabel="Category", ylabel="Revenue (IDR)")
    ax.tick_params(axis="x", rotation=25)
    rupiah_axis(ax); ax.grid(axis="y", alpha=.25); fig.tight_layout()
    fig.savefig(CHARTS / "category_revenue.png", dpi=160); plt.close(fig)

    # Chart 3: city performance
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(city["city"], city["revenue_idr"])
    ax.set(title="Revenue by City", xlabel="City", ylabel="Revenue (IDR)")
    ax.tick_params(axis="x", rotation=25)
    rupiah_axis(ax); ax.grid(axis="y", alpha=.25); fig.tight_layout()
    fig.savefig(CHARTS / "city_revenue.png", dpi=160); plt.close(fig)

    total_revenue = df["revenue_idr"].sum()
    total_profit = df["profit_idr"].sum()
    print(f"Rows analyzed: {len(df):,}")
    print(f"Total revenue: Rp{total_revenue:,.0f}")
    print(f"Estimated profit: Rp{total_profit:,.0f}")
    print(f"Profit margin: {total_profit/total_revenue:.1%}")
    print(f"Average order value: Rp{df['revenue_idr'].mean():,.0f}")
    print(f"Top category: {category.iloc[0]['category']}")
    print(f"Top city: {city.iloc[0]['city']}")

if __name__ == "__main__":
    main()
