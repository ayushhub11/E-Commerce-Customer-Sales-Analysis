import pandas as pd

df = pd.read_csv("Analysis/cleaned_sales_data.csv")
rfm = pd.read_csv("Analysis/customer_rfm_segments.csv", index_col="Customer ID")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

total_revenue = df["Sales"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["Description"].nunique()

monthly_sales = df.groupby(
    df["InvoiceDate"].dt.to_period("M")
)["Sales"].sum()

country_sales = df.groupby("Country")["Sales"].sum()

product_sales = df.groupby("Description")["Quantity"].sum()

segment_counts = rfm["Customer_Segment"].value_counts()

print("========== BUSINESS INSIGHTS ==========")

print("\nTotal Revenue:", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Unique Products:", total_products)

print("\nBest Sales Month:", monthly_sales.idxmax())
print("Highest Revenue Country:", country_sales.idxmax())
print("Best Selling Product:", product_sales.idxmax())

print("\nCustomer Segments:")
print(segment_counts)

print("\nAverage Spending by Segment:")
print(rfm.groupby("Customer_Segment")["Monetary"].mean().round(2))

print("\n========== BUSINESS RECOMMENDATIONS ==========")

print("1. Focus on retaining Champions customers.")
print("2. Create special offers for At Risk customers.")
print("3. Encourage Regular Customers to purchase more frequently.")
print("4. Focus marketing efforts on high-revenue countries.")
print("5. Promote best-selling products to increase sales.")