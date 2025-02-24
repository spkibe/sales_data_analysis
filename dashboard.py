import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Case Study Data.csv")
    # replace space with '_'
    df.columns = df.columns.str.replace(' ', '_')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['UNIT_PRICE'] = df['UNIT_PRICE'].str.replace(',', '').astype(float)
    df['SALES_VALUE'] = df['QUANTITY'] * df['UNIT_PRICE']
    df['Month-Year'] = df['DATE'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
category = st.sidebar.selectbox("Select Category", df['ANONYMIZED_CATEGORY'].unique())
business = st.sidebar.selectbox("Select Business", df['ANONYMIZED_BUSINESS'].unique())

# Filter data based on selections
filtered_df = df[(df['ANONYMIZED_CATEGORY'] == category) & (df['ANONYMIZED_BUSINESS'] == business)]

# Display filtered data
st.write("Filtered Data")
st.write(filtered_df)

# Sales Overview
st.header("Sales Overview")
total_quantity = filtered_df['QUANTITY'].sum()
total_sales_value = filtered_df['SALES_VALUE'].sum()

st.metric("Total Quantity", total_quantity)
st.metric("Total Sales Value", f"${total_sales_value:,.2f}")

# Sales Trends Over Time
st.header("Sales Trends Over Time")
monthly_sales = filtered_df.groupby('Month-Year').agg({'SALES_VALUE': 'sum', 'QUANTITY': 'sum'}).reset_index()

fig = px.line(monthly_sales, x='Month-Year', y='SALES_VALUE', title='Sales Value Over Time')
st.plotly_chart(fig)

fig = px.line(monthly_sales, x='Month-Year', y='QUANTITY', title='Quantity Sold Over Time')
st.plotly_chart(fig)

# Anonymized Category Analysis
st.header("Anonymized Category Analysis")
category_summary = df.groupby('ANONYMIZED_CATEGORY').agg(
    TOTAL_QUANTITY=('QUANTITY', 'sum'),
    TOTAL_SALES_VALUE=('SALES_VALUE', 'sum')
).reset_index()

fig = px.bar(category_summary, x='ANONYMIZED_CATEGORY', y='TOTAL_SALES_VALUE', title='Total Sales Value by Category')
st.plotly_chart(fig)

fig = px.bar(category_summary, x='ANONYMIZED_CATEGORY', y='TOTAL_QUANTITY', title='Total Quantity by Category')
st.plotly_chart(fig)

# Anonymized Business Analysis
st.header("Anonymized Business Analysis")
business_summary = df.groupby('ANONYMIZED_BUSINESS').agg(
    TOTAL_QUANTITY=('QUANTITY', 'sum'),
    TOTAL_SALES_VALUE=('SALES_VALUE', 'sum')
).reset_index()

fig = px.bar(business_summary, x='ANONYMIZED_BUSINESS', y='TOTAL_SALES_VALUE', title='Total Sales Value by Business')
st.plotly_chart(fig)

fig = px.bar(business_summary, x='ANONYMIZED_BUSINESS', y='TOTAL_QUANTITY', title='Total Quantity by Business')
st.plotly_chart(fig)