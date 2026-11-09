import pandas as pd

df = pd.read_csv("Analysis/cleaned_sales_data.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Day"] = df["InvoiceDate"].dt.day_name()

df["Hour"] = df["InvoiceDate"].dt.hour

daily_sales = df.groupby("Day")["Sales"].sum()

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

daily_sales = daily_sales.reindex(day_order)

print("Day-wise Sales Performance:")
print(daily_sales.round(2))

print("\nHighest Sales Day:")
print(daily_sales.idxmax())

print("\nHourly Sales Performance:")
print(df.groupby("Hour")["Sales"].sum().round(2))
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.bar(daily_sales.index, daily_sales.values)

plt.title("Day-wise Sales Performance")
plt.xlabel("Day")
plt.ylabel("Total Revenue")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("Visualizations/day_wise_sales.png", dpi=300)

plt.show()

hourly_sales = df.groupby("Hour")["Sales"].sum()

plt.figure(figsize=(10, 6))

plt.plot(hourly_sales.index, hourly_sales.values, marker="o")

plt.title("Hourly Sales Performance")
plt.xlabel("Hour")
plt.ylabel("Total Revenue")
plt.grid(True)
plt.tight_layout()

plt.savefig("Visualizations/hourly_sales.png", dpi=300)

plt.show()

print("\nSales trend charts saved successfully!")