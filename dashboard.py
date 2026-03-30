import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# Light background theme
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    import os
    csv_path = os.path.join(os.path.dirname(__file__), 'sales_dashboard_dataset.csv')
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Profit'] = df['Revenue'] - df['Cost']
    df['Profit_Margin'] = (df['Profit'] / df['Revenue'] * 100).round(2)
    return df

df = load_data()

# Title
st.title("📊 Sales Dashboard")
st.markdown("---")

# Calculate Key Metrics
total_revenue = df['Revenue'].sum()
total_cost = df['Cost'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_revenue * 100)
total_units = df['Quantity'].sum()
avg_order_value = total_revenue / len(df)
num_transactions = len(df)

# Display KPIs in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.0f}")

with col2:
    st.metric(label="📈 Total Profit", value=f"${total_profit:,.0f}")

with col3:
    st.metric(label="📊 Profit Margin", value=f"{profit_margin:.2f}%")

with col4:
    st.metric(label="🎯 AOV", value=f"${avg_order_value:,.0f}")

st.markdown("---")

# More KPIs
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(label="📦 Total Units Sold", value=f"{total_units:,.0f}")

with col6:
    st.metric(label="💵 Total Cost", value=f"${total_cost:,.0f}")

with col7:
    st.metric(label="🔄 Total Transactions", value=f"{num_transactions}")

with col8:
    avg_profit_margin = df['Profit_Margin'].mean()
    st.metric(label="📉 Avg Profit Margin", value=f"{avg_profit_margin:.2f}%")

st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Trends", "🏷️ By Category", "🛍️ By Product", "📅 Daily Performance", "📋 Data"])

# Tab 1: Trends
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue trend
        daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=daily_revenue['Date'],
            y=daily_revenue['Revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))
        fig_revenue.update_layout(
            title="Daily Revenue Trend",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Profit trend
        daily_profit = df.groupby('Date')['Profit'].sum().reset_index()
        fig_profit = go.Figure()
        fig_profit.add_trace(go.Scatter(
            x=daily_profit['Date'],
            y=daily_profit['Profit'],
            mode='lines+markers',
            name='Profit',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=8)
        ))
        fig_profit.update_layout(
            title="Daily Profit Trend",
            xaxis_title="Date",
            yaxis_title="Profit ($)",
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_profit, use_container_width=True)

# Tab 2: By Category
with tab2:
    category_stats = df.groupby('Category').agg({
        'Revenue': 'sum',
        'Cost': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    category_stats['Profit_Margin'] = (category_stats['Profit'] / category_stats['Revenue'] * 100).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by category
        fig_cat_revenue = px.pie(
            category_stats,
            values='Revenue',
            names='Category',
            title='Revenue Distribution by Category',
            hole=0.3
        )
        fig_cat_revenue.update_layout(height=400)
        st.plotly_chart(fig_cat_revenue, use_container_width=True)
    
    with col2:
        # Profit by category
        fig_cat_profit = go.Figure(data=[
            go.Bar(
                x=category_stats['Category'],
                y=category_stats['Profit'],
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                text=category_stats['Profit'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
            )
        ])
        fig_cat_profit.update_layout(
            title="Profit by Category",
            xaxis_title="Category",
            yaxis_title="Profit ($)",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_cat_profit, use_container_width=True)
    
    st.subheader("Category Performance Table")
    st.dataframe(
        category_stats.style.format({
            'Revenue': '${:,.0f}',
            'Cost': '${:,.0f}',
            'Profit': '${:,.0f}',
            'Profit_Margin': '{:.2f}%'
        }),
        use_container_width=True
    )

# Tab 3: By Product
with tab3:
    product_stats = df.groupby('Product').agg({
        'Revenue': 'sum',
        'Cost': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    product_stats['Profit_Margin'] = (product_stats['Profit'] / product_stats['Revenue'] * 100).round(2)
    product_stats = product_stats.sort_values('Revenue', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by product
        fig_prod_revenue = go.Figure(data=[
            go.Bar(
                x=product_stats['Product'],
                y=product_stats['Revenue'],
                marker_color='#1f77b4',
                text=product_stats['Revenue'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
            )
        ])
        fig_prod_revenue.update_layout(
            title="Revenue by Product",
            xaxis_title="Product",
            yaxis_title="Revenue ($)",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_prod_revenue, use_container_width=True)
    
    with col2:
        # Quantity by product
        fig_prod_qty = go.Figure(data=[
            go.Bar(
                x=product_stats['Product'],
                y=product_stats['Quantity'],
                marker_color='#ff7f0e',
                text=product_stats['Quantity'],
                textposition='auto',
            )
        ])
        fig_prod_qty.update_layout(
            title="Units Sold by Product",
            xaxis_title="Product",
            yaxis_title="Quantity",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_prod_qty, use_container_width=True)
    
    st.subheader("Product Performance Table")
    st.dataframe(
        product_stats.style.format({
            'Revenue': '${:,.0f}',
            'Cost': '${:,.0f}',
            'Profit': '${:,.0f}',
            'Profit_Margin': '{:.2f}%'
        }),
        use_container_width=True
    )

# Tab 4: Daily Performance
with tab4:
    daily_stats = df.groupby('Date').agg({
        'Revenue': 'sum',
        'Cost': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    daily_stats['Profit_Margin'] = (daily_stats['Profit'] / daily_stats['Revenue'] * 100).round(2)
    
    # Combo chart
    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(
        x=daily_stats['Date'],
        y=daily_stats['Revenue'],
        name='Revenue',
        marker_color='lightblue',
        yaxis='y'
    ))
    fig_combo.add_trace(go.Scatter(
        x=daily_stats['Date'],
        y=daily_stats['Profit_Margin'],
        name='Profit Margin %',
        line=dict(color='red', width=2),
        yaxis='y2',
        mode='lines+markers'
    ))
    
    fig_combo.update_layout(
        title="Daily Revenue vs Profit Margin",
        xaxis_title="Date",
        yaxis=dict(title='Revenue ($)', side='left'),
        yaxis2=dict(title='Profit Margin (%)', overlaying='y', side='right'),
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig_combo, use_container_width=True)
    
    st.subheader("Daily Performance Table")
    st.dataframe(
        daily_stats.style.format({
            'Date': lambda x: x.strftime('%Y-%m-%d'),
            'Revenue': '${:,.0f}',
            'Cost': '${:,.0f}',
            'Profit': '${:,.0f}',
            'Profit_Margin': '{:.2f}%'
        }),
        use_container_width=True
    )

# Tab 5: Raw Data
with tab5:
    st.subheader("Raw Sales Data")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_product = st.multiselect("Filter by Product", df['Product'].unique(), default=df['Product'].unique())
    
    with col2:
        selected_category = st.multiselect("Filter by Category", df['Category'].unique(), default=df['Category'].unique())
    
    with col3:
        date_range = st.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
    
    # Apply filters
    filtered_df = df[
        (df['Product'].isin(selected_product)) &
        (df['Category'].isin(selected_category)) &
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1]))
    ].copy()
    
    filtered_df = filtered_df.sort_values('Date', ascending=False)
    
    st.dataframe(
        filtered_df[['Date', 'Product', 'Category', 'Quantity', 'Revenue', 'Cost', 'Profit', 'Profit_Margin']].style.format({
            'Date': lambda x: x.strftime('%Y-%m-%d'),
            'Revenue': '${:,.0f}',
            'Cost': '${:,.0f}',
            'Profit': '${:,.0f}',
            'Profit_Margin': '{:.2f}%'
        }),
        use_container_width=True
    )
    
    # Summary statistics for filtered data
    st.subheader("Filtered Data Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", len(filtered_df))
    with col2:
        st.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
    with col3:
        st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
    with col4:
        st.metric("Avg Profit Margin", f"{filtered_df['Profit_Margin'].mean():.2f}%")

st.markdown("---")
st.markdown("📧 Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
