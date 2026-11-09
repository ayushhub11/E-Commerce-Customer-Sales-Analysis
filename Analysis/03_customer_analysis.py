import pandas as pd

df = pd.read_csv("Analysis/cleaned_sales_data.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

customer_df = df.dropna(subset=["Customer ID"]).copy()

snapshot_date = customer_df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = customer_df.groupby("Customer ID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("Sales", "sum")
)

print("RFM Customer Analysis:")
print(rfm.head(10))

print("\nRFM Summary:")
print(rfm.describe())
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    4,
    labels=[4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

print("\nRFM Scores:")
print(rfm.head(10))

print("\nRFM Score Distribution:")
print(rfm["RFM_Score"].value_counts().head(10))
def segment_customer(row):
    if row["RFM_Score"] == "444":
        return "Champions"
    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal Customers"
    elif row["R_Score"] >= 3:
        return "Recent Customers"
    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"
    else:
        return "Regular Customers"

rfm["Customer_Segment"] = rfm.apply(segment_customer, axis=1)

print("\nCustomer Segmentation:")
print(rfm["Customer_Segment"].value_counts())

print("\nSegment-wise Average Spending:")
print(rfm.groupby("Customer_Segment")["Monetary"].mean().round(2))

rfm.to_csv("Analysis/customer_rfm_segments.csv")

print("\nCustomer segmentation saved successfully!")
import matplotlib.pyplot as plt

segment_counts = rfm["Customer_Segment"].value_counts()

plt.figure(figsize=(10, 6))

plt.bar(
    segment_counts.index,
    segment_counts.values
)

plt.title("Customer Segmentation Analysis")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("Visualizations/customer_segmentation.png", dpi=300)

plt.show()

print("\nCustomer segmentation chart saved successfully!")