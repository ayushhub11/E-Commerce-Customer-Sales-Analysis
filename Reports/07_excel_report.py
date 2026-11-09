import pandas as pd
import os

df = pd.read_csv("Analysis/cleaned_sales_data.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

monthly_sales = df.groupby(
    df["InvoiceDate"].dt.to_period("M")
)["Sales"].sum().reset_index()

monthly_sales["Month"] = monthly_sales["InvoiceDate"].astype(str)
monthly_sales = monthly_sales[["Month", "Sales"]]

country_sales = df.groupby("Country").agg(
    Total_Revenue=("Sales", "sum"),
    Total_Orders=("Invoice", "nunique"),
    Total_Quantity=("Quantity", "sum"),
    Unique_Customers=("Customer ID", "nunique")
).sort_values("Total_Revenue", ascending=False)

top_products = df.groupby("Description").agg(
    Total_Quantity=("Quantity", "sum"),
    Total_Revenue=("Sales", "sum")
).sort_values("Total_Quantity", ascending=False).head(10)

rfm = pd.read_csv("Analysis/customer_rfm_segments.csv")

customer_segments = rfm["Customer_Segment"].value_counts().reset_index()
customer_segments.columns = ["Customer_Segment", "Total_Customers"]

rfm_summary = rfm.groupby("Customer_Segment").agg(
    Average_Recency=("Recency", "mean"),
    Average_Frequency=("Frequency", "mean"),
    Average_Monetary=("Monetary", "mean"),
    Total_Customers=("Customer_Segment", "count")
).round(2)

business_summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Orders",
        "Total Customers",
        "Unique Products"
    ],
    "Value": [
        round(df["Sales"].sum(), 2),
        df["Invoice"].nunique(),
        df["Customer ID"].nunique(),
        df["Description"].nunique()
    ]
})

os.makedirs("Reports", exist_ok=True)

with pd.ExcelWriter("Reports/Ecommerce_Analysis_Report.xlsx", engine="openpyxl") as writer:
    business_summary.to_excel(writer, sheet_name="Business Summary", index=False)
    monthly_sales.to_excel(writer, sheet_name="Monthly Sales", index=False)
    country_sales.to_excel(writer, sheet_name="Country Analysis")
    top_products.to_excel(writer, sheet_name="Top Products")
    customer_segments.to_excel(writer, sheet_name="Customer Segments", index=False)
    rfm_summary.to_excel(writer, sheet_name="RFM Analysis")

print("Excel Report Created Successfully!")
print("File: Reports/Ecommerce_Analysis_Report.xlsx")