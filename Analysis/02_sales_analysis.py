import pandas as pd

df = pd.read_csv("Analysis/cleaned_sales_data.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()

monthly_sales["Month"] = monthly_sales["Month"].astype(str)

print("Monthly Sales Performance:")
print(monthly_sales)

print("\nHighest Sales Month:")
print(monthly_sales.loc[monthly_sales["Sales"].idxmax()])
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Month"],
    monthly_sales["Sales"],
    marker="o"
)

plt.title("Monthly Sales Performance")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("Visualizations/monthly_sales.png", dpi=300)

plt.show()
country_sales = df.groupby("Country")["Sales"].sum().sort_values(ascending=False)

print("\nTop 10 Countries by Revenue:")
print(country_sales.head(10))

print("\nHighest Revenue Country:")
print(country_sales.idxmax())
top_countries = country_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))

plt.barh(top_countries.index, top_countries.values)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("Visualizations/top_10_countries.png", dpi=300)

plt.show()
top_products = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Best-Selling Products:")
print(top_products)
top_products = top_products.sort_values()

plt.figure(figsize=(12, 7))

plt.barh(top_products.index, top_products.values)

plt.title("Top 10 Best-Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("Visualizations/top_10_products.png", dpi=300)

plt.show()
customer_df = df.dropna(subset=["Customer ID"])

customer_sales = customer_df.groupby("Customer ID").agg(
    Total_Spending=("Sales", "sum"),
    Total_Orders=("Invoice", "nunique"),
    Total_Quantity=("Quantity", "sum")
)

print("\nTotal Unique Customers:", customer_df["Customer ID"].nunique())

print("\nTop 10 Customers by Spending:")
print(customer_sales.sort_values("Total_Spending", ascending=False).head(10))