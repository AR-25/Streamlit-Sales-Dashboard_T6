
import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --- DATA LOADING AND CLEANING ---
@st.cache_data
def load_data():
    df = pd.read_csv('supermarket_sales.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
    # Rename 'gross income' for easier access
    df.rename(columns={'gross income': 'Gross_Income'}, inplace=True)
    return df

df = load_data()

# --- SIDEBAR FOR FILTERS ---
st.sidebar.header("Filter Your Data")

city = st.sidebar.multiselect(
    "Select City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select Customer Type:",
    options=df["Customer type"].unique(),
    default=df["Customer type"].unique()
)

# Filter the dataframe based on selection
df_selection = df.query(
    "City == @city and `Customer type` == @customer_type"
)

# --- MAIN PAGE ---
st.title("🛒 Supermarket Sales Dashboard")
st.markdown("##")

# --- KEY METRICS (KPIs) ---
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
total_gross_income = int(df_selection["Gross_Income"].sum())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} ⭐")
with right_column:
    st.subheader("Total Gross Income:")
    st.subheader(f"US $ {total_gross_income:,}")

st.markdown("---")

# --- CHARTS ---

# Sales by Product Line (Bar Chart)
sales_by_product_line = df_selection.groupby("Product line")["Total"].sum().sort_values()
fig_product_sales = px.bar(
    sales_by_product_line,
    x=sales_by_product_line.values,
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    template="plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Total Sales",
    yaxis_title="Product Line"
)

# Gross Income by Product Line (Bar Chart)
gross_income_by_product_line = df_selection.groupby("Product line")["Gross_Income"].sum().sort_values()
fig_gross_income = px.bar(
    gross_income_by_product_line,
    x=gross_income_by_product_line.values,
    y=gross_income_by_product_line.index,
    orientation="h",
    title="<b>Gross Income by Product Line</b>",
    template="plotly_white"
)
fig_gross_income.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Total Gross Income",
    yaxis_title="Product Line"
)

# Place charts side-by-side
left_chart, right_chart = st.columns(2)
left_chart.plotly_chart(fig_product_sales, use_container_width=True)
right_chart.plotly_chart(fig_gross_income, use_container_width=True)
