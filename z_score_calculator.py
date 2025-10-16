import pandas as pd
import numpy as np

# Load Excel
excel_path = "GeoHealth-lung function 16Oct2025.xlsx"
df = pd.read_excel(excel_path, sheet_name="Sheet1")

# Load CSV with M and S reference values
ref_df = pd.read_csv("FEV1:FVC ratio.csv")

# Calculate L for each subject
df["L"] = 6.6490 - 0.9920 * np.log(df["Age_years"])

# Interpolate M and S based on subject Age
df = df.merge(ref_df, how="left", left_on="Age_years", right_on="Age")

# Calculate Z-score
df["Z-score"] = (((df["Ration_FEV1_FVC"] / df["M"]) ** df["L"]) - 1) / (df["L"] * df["S"])

# Put Z-score as the last (rightmost) column
cols = [c for c in df.columns if c != "Z-score"] + ["Z-score"]
df = df[cols]

# Save to CSV
output_path = "GeoHealth-lung function_with_Zscore.csv"
df.to_csv(output_path, index=False)

print("Saved:", output_path)