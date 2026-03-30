from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


DATA_PATH = Path(__file__).with_name("sales_dashboard_dataset.csv")
COLORWAY = ["#14b8a6", "#f97316", "#38bdf8", "#f59e0b", "#fb7185"]


st.markdown(
    """
    <style>
        .stApp {
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
            background:
                radial-gradient(circle at top right, rgba(56, 189, 248, 0.16), transparent 28%),
                radial-gradient(circle at top left, rgba(251, 113, 133, 0.12), transparent 25%),
                linear-gradient(180deg, #fffaf5 0%, #f4fbfb 100%);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fffaf5 0%, #f5fbfb 100%);
            border-right: 1px solid rgba(15, 23, 42, 0.08);
        }
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(20, 184, 166, 0.18);
            border-radius: 18px;
            padding: 14px 16px;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
        }
        div[data-testid="stMetricLabel"] {
            font-weight: 700;
        }
        .metric-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.8rem;
            margin: 0.25rem 0 1rem;
        }
        .metric-badge {
            border-radius: 18px;
            padding: 0.95rem 1rem;
            color: #0f172a;
            box-shadow: 0 14px 28px rgba(15, 23, 42, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }
        .metric-badge h3 {
            margin: 0;
            font-size: 0.88rem;
            color: #334155;
        }
        .metric-badge .big {
            margin-top: 0.3rem;
            font-size: 1.55rem;
            font-weight: 800;
        }
        .metric-badge .small {
            margin-top: 0.2rem;
            font-size: 0.88rem;
            color: #475569;
        }
        .bg-teal { background: linear-gradient(135deg, #ccfbf1 0%, #f0fdfa 100%); }
        .bg-orange { background: linear-gradient(135deg, #ffedd5 0%, #fff7ed 100%); }
        .bg-blue { background: linear-gradient(135deg, #dbeafe 0%, #f0f9ff 100%); }
        .bg-pink { background: linear-gradient(135deg, #ffe4e6 0%, #fff1f2 100%); }
        .section-card {
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 22px;
            padding: 1rem 1.1rem 0.5rem;
            box-shadow: 0 16px 34px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }
        .story-card {
            background: linear-gradient(135deg, #fff1df 0%, #e6faf7 100%);
            color: #0f172a;
            border-radius: 24px;
            padding: 1.25rem 1.4rem;
            border: 1px solid rgba(249, 115, 22, 0.14);
            box-shadow: 0 18px 32px rgba(15, 23, 42, 0.05);
            margin: 0.35rem 0 1rem;
        }
        .story-card h2 {
            margin: 0 0 0.45rem;
            font-size: 1.25rem;
        }
        .story-card p {
            margin: 0;
            color: #334155;
            font-size: 0.98rem;
            line-height: 1.5;
        }
        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin: 0.9rem 0 0;
        }
        .pill {
            border-radius: 999px;
            padding: 0.42rem 0.8rem;
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(20, 184, 166, 0.14);
            font-size: 0.9rem;
            color: #0f172a;
        }
        .subtle-label {
            color: #475569;
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.2rem;
        }
        .section-title {
            margin: 0.2rem 0 0.75rem;
            font-size: 1.1rem;
            color: #0f172a;
            font-weight: 700;
        }
        .insight-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 0.4rem 0 1rem;
        }
        .insight-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.12);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            box-shadow: 0 14px 28px rgba(15, 23, 42, 0.05);
        }
        .insight-card h3 {
            margin: 0 0 0.3rem;
            font-size: 0.95rem;
            color: #0f172a;
        }
        .insight-card .value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #f97316;
            margin-bottom: 0.15rem;
        }
        .insight-card p {
            margin: 0;
            color: #475569;
            font-size: 0.93rem;
        }
        .hero {
            padding: 1.4rem 1.5rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #0ea5e9 0%, #14b8a6 52%, #f97316 100%);
            color: white;
            box-shadow: 0 18px 38px rgba(20, 184, 166, 0.22);
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.2rem;
            line-height: 1.1;
        }
        .hero p {
            margin: 0.45rem 0 0;
            color: rgba(255, 255, 255, 0.84);
            font-size: 1rem;
        }
        div[data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        button[data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 999px;
            padding: 0.45rem 1rem;
            border: 1px solid rgba(15, 23, 42, 0.08);
        }
        @media (max-width: 900px) {
            .metric-strip,
            .insight-grid {
                grid-template-columns: 1fr;
            }
            .hero {
                padding: 1.15rem 1rem;
            }
            .hero h1 {
                font-size: 1.7rem;
            }
            .section-card {
                padding: 0.9rem 0.8rem 0.4rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Revenue"] = pd.to_numeric(df["Revenue"])
    df["Cost"] = pd.to_numeric(df["Cost"])
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit Margin %"] = (df["Profit"] / df["Revenue"] * 100).round(2)
    df["Unit Price"] = (df["Revenue"] / df["Quantity"]).round(2)
    df["Unit Cost"] = (df["Cost"] / df["Quantity"]).round(2)
    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["Week"] = df["Date"].dt.to_period("W").apply(lambda period: period.start_time)
    return df.sort_values("Date")


def currency(value: float) -> str:
    return f"Rs {value:,.0f}"


def percentage(value: float) -> str:
    return f"{value:.2f}%"


def build_metric_delta(current: float, baseline: float) -> str:
    if baseline == 0:
        return "N/A"
    change = ((current - baseline) / baseline) * 100
    return f"{change:+.1f}%"


def delta_text(current: float, baseline: float) -> str:
    if baseline == 0:
        return "No previous period"
    return f"vs previous period {build_metric_delta(current, baseline)}"


def style_chart(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        margin=dict(l=10, r=10, t=56, b=10),
        font=dict(color="#0f172a"),
    )
    return fig


df = load_data(DATA_PATH)

st.markdown(
    """
    <div class="hero">
        <h1>Sales Performance Dashboard</h1>
        <p>Interactive view of revenue, profit, margins, product mix, and daily sales performance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Filters")
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if len(date_range) != 2:
        date_range = (min_date, max_date)

    category_options = sorted(df["Category"].unique().tolist())
    product_options = sorted(df["Product"].unique().tolist())

    selected_categories = st.multiselect(
        "Category",
        options=category_options,
        default=category_options,
    )
    selected_products = st.multiselect(
        "Product",
        options=product_options,
        default=product_options,
    )

    st.caption("Tip: narrow to a category or product to see focused KPIs and trends.")


filtered_df = df[
    df["Date"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))
    & df["Category"].isin(selected_categories)
    & df["Product"].isin(selected_products)
].copy()

if filtered_df.empty:
    st.warning("No rows match the current filters. Adjust the sidebar selections to continue.")
    st.stop()


selected_period = filtered_df["Date"].max() - filtered_df["Date"].min()
comparison_start = filtered_df["Date"].min() - selected_period - pd.Timedelta(days=1)
comparison_end = filtered_df["Date"].min() - pd.Timedelta(days=1)
comparison_df = df[
    df["Date"].between(comparison_start, comparison_end)
    & df["Category"].isin(selected_categories)
    & df["Product"].isin(selected_products)
].copy()

total_revenue = filtered_df["Revenue"].sum()
total_cost = filtered_df["Cost"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = int(filtered_df["Quantity"].sum())
transaction_count = int(len(filtered_df))
avg_order_value = total_revenue / transaction_count
avg_unit_price = filtered_df["Revenue"].sum() / filtered_df["Quantity"].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

comparison_revenue = comparison_df["Revenue"].sum() if not comparison_df.empty else 0
comparison_profit = comparison_df["Profit"].sum() if not comparison_df.empty else 0
comparison_margin = (
    (comparison_profit / comparison_revenue) * 100 if comparison_revenue else 0
)

monthly_summary = (
    filtered_df.groupby("Month", as_index=False)[["Revenue", "Cost", "Profit", "Quantity"]]
    .sum()
    .sort_values("Month")
)
monthly_summary["Profit Margin %"] = (
    monthly_summary["Profit"] / monthly_summary["Revenue"] * 100
).round(2)

daily_summary = (
    filtered_df.groupby("Date", as_index=False)[["Revenue", "Cost", "Profit", "Quantity"]]
    .sum()
    .sort_values("Date")
)
daily_summary["Profit Margin %"] = (
    daily_summary["Profit"] / daily_summary["Revenue"] * 100
).round(2)

category_summary = (
    filtered_df.groupby("Category", as_index=False)[["Revenue", "Cost", "Profit", "Quantity"]]
    .sum()
    .sort_values("Revenue", ascending=False)
)
category_summary["Profit Margin %"] = (
    category_summary["Profit"] / category_summary["Revenue"] * 100
).round(2)
category_summary["Share %"] = (category_summary["Revenue"] / total_revenue * 100).round(1)

product_summary = (
    filtered_df.groupby(["Product", "Category"], as_index=False)[["Revenue", "Cost", "Profit", "Quantity"]]
    .sum()
    .sort_values("Revenue", ascending=False)
)
product_summary["Profit Margin %"] = (
    product_summary["Profit"] / product_summary["Revenue"] * 100
).round(2)
product_summary["Avg Unit Price"] = (product_summary["Revenue"] / product_summary["Quantity"]).round(2)

top_product = product_summary.iloc[0]
top_category = category_summary.iloc[0]
best_margin_product = product_summary.sort_values("Profit Margin %", ascending=False).iloc[0]
lowest_margin_product = product_summary.sort_values("Profit Margin %", ascending=True).iloc[0]
avg_daily_revenue = daily_summary["Revenue"].mean()
best_day = daily_summary.sort_values("Revenue", ascending=False).iloc[0]
top_products = product_summary.head(5).copy()
top_products["Share %"] = (top_products["Revenue"] / total_revenue * 100).round(1)
category_share = category_summary.copy()
monthly_revenue_change = (
    monthly_summary["Revenue"].pct_change().iloc[-1] * 100
    if len(monthly_summary) > 1
    else 0
)

st.markdown(
    f"""
    <div class="metric-strip">
        <div class="metric-badge bg-teal">
            <h3>Revenue</h3>
            <div class="big">{currency(total_revenue)}</div>
            <div class="small">{delta_text(total_revenue, comparison_revenue)}</div>
        </div>
        <div class="metric-badge bg-orange">
            <h3>Profit</h3>
            <div class="big">{currency(total_profit)}</div>
            <div class="small">{delta_text(total_profit, comparison_profit)}</div>
        </div>
        <div class="metric-badge bg-blue">
            <h3>Profit Margin</h3>
            <div class="big">{percentage(profit_margin)}</div>
            <div class="small">{delta_text(profit_margin, comparison_margin)}</div>
        </div>
        <div class="metric-badge bg-pink">
            <h3>Avg Order Value</h3>
            <div class="big">{currency(avg_order_value)}</div>
            <div class="small">{transaction_count:,} transactions in view</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols_2 = st.columns(4)
metric_cols_2[0].metric("Cost", currency(total_cost))
metric_cols_2[1].metric("Units", f"{total_quantity:,}")
metric_cols_2[2].metric("Orders", f"{transaction_count:,}")
metric_cols_2[3].metric("Avg Unit Price", f"Rs {avg_unit_price:,.0f}")

with st.sidebar:
    st.markdown("---")
    st.markdown("### Quick Read")
    st.markdown(
        f"""
        - Revenue leader: **{top_product['Product']}**
        - Strongest margin: **{best_margin_product['Product']}**
        - Biggest category: **{top_category['Category']}**
        - Best day: **{best_day['Date']:%d %b %Y}**
        """
    )

st.markdown(
    f"""
    <div class="story-card">
        <h2>Executive Snapshot</h2>
        <p>
            <strong>{top_product['Product']}</strong> leads sales,
            <strong>{top_category['Category']}</strong> is the biggest category,
            and <strong>{best_margin_product['Product']}</strong> delivers the best margin.
        </p>
        <div class="pill-row">
            <div class="pill">Monthly revenue change: {monthly_revenue_change:+.1f}%</div>
            <div class="pill">Best margin: {best_margin_product['Product']} at {percentage(best_margin_product['Profit Margin %'])}</div>
            <div class="pill">Watchlist: {lowest_margin_product['Product']} at {percentage(lowest_margin_product['Profit Margin %'])}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="subtle-label">Quick Highlights</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="insight-grid">
        <div class="insight-card">
            <h3>Top Product</h3>
            <div class="value">{top_product['Product']}</div>
            <p>{currency(top_product['Revenue'])} revenue across {int(top_product['Quantity'])} units</p>
        </div>
        <div class="insight-card">
            <h3>Top Category</h3>
            <div class="value">{top_category['Category']}</div>
            <p>{currency(top_category['Revenue'])} revenue with {percentage(top_category['Profit Margin %'])} margin</p>
        </div>
        <div class="insight-card">
            <h3>Best Sales Day</h3>
            <div class="value">{best_day['Date']:%d %b}</div>
            <p>{currency(best_day['Revenue'])} revenue, above avg daily revenue of {currency(avg_daily_revenue)}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_overview, tab_drivers, tab_data = st.tabs(
    ["Overview", "What Drives Sales", "Detailed Data"]
)

with tab_overview:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">At-a-glance performance</div>', unsafe_allow_html=True)
    left_chart, right_chart = st.columns(2)

    with left_chart:
        revenue_trend = px.line(
            daily_summary,
            x="Date",
            y=["Revenue", "Profit"],
            markers=True,
            color_discrete_sequence=[COLORWAY[0], COLORWAY[1]],
            title="Revenue vs Profit",
        )
        revenue_trend.update_layout(legend_title_text="", hovermode="x unified")
        style_chart(revenue_trend, height=420)
        st.plotly_chart(revenue_trend, width="stretch")

    with right_chart:
        monthly_margin = px.bar(
            monthly_summary,
            x="Month",
            y="Revenue",
            text="Revenue",
            color_discrete_sequence=[COLORWAY[3]],
            title="Monthly Revenue",
        )
        monthly_margin.add_scatter(
            x=monthly_summary["Month"],
            y=monthly_summary["Profit Margin %"],
            name="Profit Margin %",
            mode="lines+markers+text",
            text=monthly_summary["Profit Margin %"].map(lambda value: f"{value:.1f}%"),
            textposition="top center",
            line=dict(color=COLORWAY[1], width=3),
            yaxis="y2",
        )
        monthly_margin.update_traces(
            selector=dict(type="bar"),
            texttemplate="Rs %{text:,.0f}",
            textposition="outside",
        )
        monthly_margin.update_layout(
            hovermode="x unified",
            yaxis=dict(title="Revenue"),
            yaxis2=dict(title="Profit Margin %", overlaying="y", side="right"),
        )
        style_chart(monthly_margin, height=420)
        st.plotly_chart(monthly_margin, width="stretch")

    monthly_cols = st.columns(2)
    with monthly_cols[0]:
        category_chart = px.bar(
            category_share,
            x="Revenue",
            y="Category",
            orientation="h",
            text="Share %",
            color="Category",
            color_discrete_sequence=COLORWAY,
            title="Revenue by Category",
        )
        category_chart.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        category_chart.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
        style_chart(category_chart)
        st.plotly_chart(category_chart, width="stretch")

    with monthly_cols[1]:
        product_chart = px.bar(
            top_products.sort_values("Revenue"),
            x="Revenue",
            y="Product",
            orientation="h",
            text="Share %",
            color_discrete_sequence=[COLORWAY[0]],
            title="Top Products",
        )
        product_chart.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        style_chart(product_chart)
        st.plotly_chart(product_chart, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_drivers:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Where profit and margin come from</div>', unsafe_allow_html=True)
    driver_cols = st.columns([1.1, 1.3])

    with driver_cols[0]:
        margin_chart = px.bar(
            product_summary.head(8).sort_values("Profit Margin %"),
            x="Profit Margin %",
            y="Product",
            orientation="h",
            color="Category",
            color_discrete_sequence=COLORWAY,
            title="Best Margins",
        )
        margin_chart.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
        style_chart(margin_chart, height=430)
        st.plotly_chart(margin_chart, width="stretch")

    with driver_cols[1]:
        profit_chart = px.bar(
            product_summary.head(8).sort_values("Profit"),
            x="Profit",
            y="Product",
            orientation="h",
            color="Category",
            color_discrete_sequence=COLORWAY,
            title="Top Profit Products",
        )
        profit_chart.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
        style_chart(profit_chart, height=430)
        st.plotly_chart(profit_chart, width="stretch")

    summary_cols = st.columns(2)

    with summary_cols[0]:
        st.markdown("#### Category Summary")
        st.dataframe(
            category_summary[["Category", "Revenue", "Profit", "Profit Margin %", "Quantity"]].style.format(
                {
                    "Revenue": "Rs {:,.0f}",
                    "Profit": "Rs {:,.0f}",
                    "Profit Margin %": "{:.2f}%",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    with summary_cols[1]:
        st.markdown("#### Product Summary")
        compact_products = product_summary[
            ["Product", "Category", "Revenue", "Profit", "Profit Margin %", "Quantity"]
        ].copy()
        st.dataframe(
            compact_products.style.format(
                {
                    "Revenue": "Rs {:,.0f}",
                    "Profit": "Rs {:,.0f}",
                    "Profit Margin %": "{:.2f}%",
                }
            ),
            width="stretch",
            hide_index=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Daily operating rhythm</div>', unsafe_allow_html=True)
    trend_focus_cols = st.columns(2)
    with trend_focus_cols[0]:
        qty_chart = px.area(
            daily_summary,
            x="Date",
            y="Quantity",
            color_discrete_sequence=[COLORWAY[0]],
            title="Units Over Time",
        )
        style_chart(qty_chart, height=360)
        st.plotly_chart(qty_chart, width="stretch")

    with trend_focus_cols[1]:
        daily_margin_chart = px.bar(
            daily_summary,
            x="Date",
            y="Profit",
            color_discrete_sequence=[COLORWAY[1]],
            title="Daily Profit",
        )
        style_chart(daily_margin_chart, height=360)
        st.plotly_chart(daily_margin_chart, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_data:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Detailed transaction view</div>', unsafe_allow_html=True)
    export_df = filtered_df.sort_values("Date", ascending=False)[
        [
            "Date",
            "Product",
            "Category",
            "Quantity",
            "Revenue",
            "Cost",
            "Profit",
            "Profit Margin %",
            "Unit Price",
        ]
    ].copy()

    st.dataframe(
        export_df.style.format(
            {
                "Date": lambda date: date.strftime("%d-%m-%Y"),
                "Revenue": "Rs {:,.0f}",
                "Cost": "Rs {:,.0f}",
                "Profit": "Rs {:,.0f}",
                "Profit Margin %": "{:.2f}%",
                "Unit Price": "Rs {:,.0f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_bytes,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    f"Dataset rows in view: {len(filtered_df):,} of {len(df):,} | Date coverage: "
    f"{filtered_df['Date'].min():%d %b %Y} to {filtered_df['Date'].max():%d %b %Y}"
)
