import pandas as pd

file_path = "Dataset/online_retail_II.xlsx"

df = pd.read_excel(file_path, sheet_name="Year 2009-2010")

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset Information:")
print(df.info())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Records:")
print(df.duplicated().sum())
df_cleaned = df.drop_duplicates().copy()

print("\nOriginal Rows:", len(df))
print("Rows After Removing Duplicates:", len(df_cleaned))
print("Duplicates Removed:", len(df) - len(df_cleaned))
df_cleaned = df_cleaned.dropna(subset=["Description"])

print("\nRows After Removing Missing Descriptions:", len(df_cleaned))
print("\nMissing Customer IDs:", df_cleaned["Customer ID"].isnull().sum())
print("Available Customer IDs:", df_cleaned["Customer ID"].notnull().sum())
df_cleaned["Sales"] = df_cleaned["Quantity"] * df_cleaned["Price"]

print("\nSales Column Added:")
print(df_cleaned[["Quantity", "Price", "Sales"]].head())
print("\nNegative Quantity:", (df_cleaned["Quantity"] < 0).sum())
print("Zero or Negative Price:", (df_cleaned["Price"] <= 0).sum())
cancelled = df_cleaned["Invoice"].astype(str).str.startswith("C")

print("\nCancelled Transactions:", cancelled.sum())
print("Normal Transactions:", (~cancelled).sum())
df_sales = df_cleaned[~cancelled].copy()

print("\nSales Dataset Shape:", df_sales.shape)
print("Negative Quantities in Sales:", (df_sales["Quantity"] < 0).sum())
negative_sales = df_sales[df_sales["Quantity"] < 0]

print("\nNegative Quantity Records:")
print(negative_sales[["Invoice", "Quantity", "Price", "Sales"]].head(10))
print("\nNegative Quantity Price Breakdown:")
print(df_sales[df_sales["Quantity"] < 0]["Price"].value_counts().head(10))

print("\nNegative Quantity with Positive Price:")
print(((df_sales["Quantity"] < 0) & (df_sales["Price"] > 0)).sum())
df_sales = df_sales[
    (df_sales["Quantity"] > 0) &
    (df_sales["Price"] > 0)
].copy()

print("\nFinal Sales Dataset Shape:", df_sales.shape)
print("Remaining Negative Quantities:", (df_sales["Quantity"] < 0).sum())
print("Remaining Zero or Negative Prices:", (df_sales["Price"] <= 0).sum())
print("Total Revenue:", round(df_sales["Sales"].sum(), 2))
import os

os.makedirs("Analysis", exist_ok=True)

df_sales.to_csv("Analysis/cleaned_sales_data.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("File: Analysis/cleaned_sales_data.csv")