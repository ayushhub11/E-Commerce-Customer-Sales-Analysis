import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Analysis/cleaned_sales_data.csv")

country_analysis = df.groupby("Country").agg(
    Total_Revenue=("Sales", "sum"),
    Total_Orders=("Invoice", "nunique"),
    Total_Quantity=("Quantity", "sum"),
    Unique_Customers=("Customer ID", "nunique")
)

country_analysis = country_analysis.sort_values(
    "Total_Revenue",
    ascending=False
)

print("Top 10 Countries Analysis:")
print(country_analysis.head(10).round(2))

print("\nCountry with Highest Revenue:")
print(country_analysis["Total_Revenue"].idxmax())

print("\nCountry with Most Customers:")
print(country_analysis["Unique_Customers"].idxmax())

country_analysis.to_csv("Analysis/country_wise_analysis.csv")

print("\nCountry analysis saved successfully!")
top_countries = country_analysis.head(10).sort_values("Total_Revenue")

plt.figure(figsize=(11, 7))

plt.barh(
    top_countries.index,
    top_countries["Total_Revenue"]
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig("Visualizations/country_revenue_analysis.png", dpi=300)

plt.show()

print("\nCountry revenue chart saved successfully!")