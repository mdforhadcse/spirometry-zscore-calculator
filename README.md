# Spirometry Z-Score Calculator (FEV1/FVC) (GeoHealth-lung function_with_Zscore)

A tiny, reproducible Python script that calculates the **FEV1/FVC Z-score** for each subject from an Excel sheet using LMS (Lambda–Mu–Sigma) equations. It reads measured spirometry data, looks up reference **M** and **S** values from a CSV, computes **L**, and writes a CSV with Z-scores.

This README is written so non‑technical users can follow along and get results.

---

## 🔧 Python Version
- **Python 3.12** (tested). Should also work on Python 3.9+.

---

## 📦 Used Libraries / Modules
- **pandas** – read Excel/CSV and write CSV  
- **numpy** – math (natural log, power)  
- **openpyxl** – engine used by pandas to read `.xlsx`

Install them with:
```bash
pip install pandas numpy openpyxl
```

---

## 🧮 Equations

### 1) L (Lambda) – skewness parameter
We compute **L** from age (in years):
\[ L = 6.6490 - 0.9920 \cdot \ln(\text{Age}) \]

### 2) FEV1/FVC Z-score (LMS method)
Let **Measured** be the subject’s observed FEV1/FVC ratio, and **M** (median/predicted) and **S** (sigma, coefficient of variation) come from your reference table.

\[ Z_{\text{FEV1/FVC}} = \frac{\left(\dfrac{\text{Measured}}{M}\right)^{L} - 1}{L \cdot S} \]

> Interpretation (rule of thumb): Z ≈ 0 → at the reference median; Z ≤ −1.64 → below the lower limit of normal (≈ 5th percentile).

---

## 📁 Files in this Repo

- **`z_score_calculator.py`**  
  The script. Reads your Excel and reference CSV, computes **L** and **Z-score**, and writes the output CSV.

- **`GeoHealth-lung function 16Oct2025.xlsx`** *(example input)*  
  Your measurement data. Expected columns (minimum):
  - `Round_II_study_ID` (ID)  
  - `Sex` (Male/Female)  
  - `Age_years` (Age in years; integers OK)  
  - `Height`, `Weight` (optional for this calc)  
  - `FEV1`, `FVC`  
  - `Ration_FEV1_FVC` *(measured FEV1/FVC ratio)*

- **`FEV1:FVC ratio.csv`** *(reference table)*  
  Age-based reference values with columns:
  - `Age` (years, may be fractional like 3.00, 3.25, …)  
  - `M` (median/predicted FEV1/FVC)  
  - `S` (sigma)

- **`GeoHealth-lung function_with_Zscore.csv`** *(output)*  
  The result file produced by the script. It contains all original columns plus **`Z-score`** (placed as the right-most column). The helper column `Age` from the reference file is removed in the output.

---

## 🔁 Calculation Process (What the Script Does)

1. **Load inputs**
   - Excel: `GeoHealth-lung function 16Oct2025.xlsx` (Sheet1)  
   - CSV: `FEV1:FVC ratio.csv` (reference table with Age, M, S)

2. **Compute L**  
   - For each row: `L = 6.6490 - 0.9920 * ln(Age_years)`

3. **Join reference values**  
   - Merge the subject’s `Age_years` with the CSV’s `Age` to bring in `M` and `S`.
   - (If your ages are integers and your reference CSV uses quarter-year steps, make sure they align or pre-map to the closest available age.)

4. **Compute Z-score**  
   - Using the LMS formula above for FEV1/FVC.

5. **Tidy columns**  
   - Put `Z-score` at the far right.  
   - Drop the reference `Age` helper column from the output.

6. **Save output**  
   - Writes `GeoHealth-lung function_with_Zscore.csv`.

---

## ▶️ How to Run

1) **Clone or download** this repo.  
2) **Install dependencies**:
```bash
pip install pandas numpy openpyxl
```
3) **Place your files** (or use the provided examples):
   - `GeoHealth-lung function 16Oct2025.xlsx`
   - `FEV1:FVC ratio.csv`
4) **Run the script**:
```bash
python z_score_calculator.py
```
5) **Get your results** in:
```
GeoHealth-lung function_with_Zscore.csv
```

---

## 📤 Output (What You’ll See)

- A CSV with your original subject rows plus a **`Z-score`** column on the far right.
- Example (columns abbreviated):

| Round_II_study_ID | Sex | Age_years | FEV1 | FVC | Ration_FEV1_FVC | … | Z-score |
|---|---|---:|---:|---:|---:|---|---:|
| GAA1101 | Female | 61 | 1.387 | 1.972 | 0.7033 | … | -1.92 |
| GAA1102 | Female | 47 | 2.132 | 2.558 | 0.8334 | … | -0.44 |
| … | … | … | … | … | … | … | … |

---

## ❗️ Notes & Troubleshooting

- **Reference table quality matters.**  
  Z-scores depend on correct **M** and **S**. If M or S are **missing or negative**, Z-scores may be blank (NaN). Ensure your `FEV1:FVC ratio.csv` contains valid, **positive** M and S across your age range.

- **Age alignment.**  
  If your subject ages are integers (e.g., 43, 44) but the reference uses quarter years (e.g., 43.00, 43.25…), make sure they align. You can pre-map to the nearest reference age or supply a CSV that matches your ages exactly.

- **GLI 2012 vs GLI 2022 Race‑Neutral.**  
  This script will compute Z-scores using whatever **M** and **S** you provide. If you want to match a specific external calculator (e.g., 2022 race-neutral GLI), use the corresponding official reference values for **M** and **S**.

---

## 📄 License
MIT (or your preferred license)

---

## 🙋 Need Help?
Open an issue with:
- A few sample rows from your Excel  
- The matching rows from your reference CSV  
- What result you expected vs what you got

Happy analyzing!
