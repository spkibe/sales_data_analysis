import kwanza_dashboard
from kwanza_dashboard import dcc, html
import plotly.express as px
import pandas as pd

# Load the dataset (Replace 'your_data.csv' with the actual file)
df = pd.read_csv("clean_case_study_data.csv")

# Ensure 'Month-Year' column is of the correct format (you can adjust this based on your data)
df['Month-Year'] = pd.to_datetime(df['DATE']).dt.strftime('%b-%Y')

# Calculate additional columns: Total Sales Value (QUANTITY * UNIT_PRICE)
df['Total Sales Value'] = df['QUANTITY'] * df['UNIT_PRICE']

# Create aggregated data for total quantity and sales value by category and month
category_month_df = df.groupby(['Month-Year', 'ANONYMIZED_CATEGORY']).agg(
    Total_Quantity=('QUANTITY', 'sum'),
    Total_Sales_Value=('Total Sales Value', 'sum')
).reset_index()

# Sample time-series data (sum of Total Sales Value per month for trend analysis)
time_series_data = df.groupby('Month-Year').agg(
    Total_Sales_Value=('Total Sales Value', 'sum')
).reset_index()

# Sample customer segmentation data (you can adjust based on your actual data)
# Here we assume customer segmentation data is provided separately, or you can calculate it as needed
customer_data = {
    "Segment": ["High Value", "Medium Value", "Low Value"],
    "Total Customers": [50, 120, 300]
}
customer_df = pd.DataFrame(customer_data)

# Initialize the Dash app
app = kwanza_dashboard.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    # Dropdown for selecting Month-Year
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': month} for month in df['Month-Year'].unique()],
        value=df['Month-Year'].unique()[0],
        clearable=False
    ),

    dcc.Graph(id="sales-bar-chart"),
    dcc.Graph(id="sales-trend-chart"),
    dcc.Graph(id="customer-segmentation-chart")
])

# Callback to update graphs based on selected month
@app.callback(
    [
        kwanza_dashboard.Output("sales-bar-chart", "figure"),
        kwanza_dashboard.Output("sales-trend-chart", "figure"),
        kwanza_dashboard.Output("customer-segmentation-chart", "figure")
    ],
    [kwanza_dashboard.Input("month-dropdown", "value")]
)
def update_charts(selected_month):
    # Filter data based on the selected month
    filtered_df = category_month_df[category_month_df['Month-Year'] == selected_month]
    filtered_time_df = time_series_data[time_series_data['Month-Year'] == selected_month]
    
    # Bar chart: Total Quantity & Total Sales Value by Category
    bar_chart = px.bar(filtered_df, x="ANONYMIZED_CATEGORY", y=["Total_Quantity", "Total_Sales_Value"],
                        barmode="group", title="Total Quantity & Sales Value by Category")
    
    # Line chart: Total Sales Value trend over time
    line_chart = px.line(time_series_data, x="Month-Year", y="Total_Sales_Value",
                         title="Sales Trend Over Time")
    
    # Pie chart: Customer Segmentation (Adjust this if you have actual data for segmentation)
    pie_chart = px.pie(customer_df, names="Segment", values="Total Customers",
                        title="Customer Segmentation")

    return bar_chart, line_chart, pie_chart

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
