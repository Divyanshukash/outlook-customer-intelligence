from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. FIND PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------
# 2. DEFINE EXCEL FILE LOCATION
# ---------------------------------------------------------

EXCEL_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "outlook_consumer_survey.xlsx"
)


# ---------------------------------------------------------
# 3. CHECK WHETHER FILE EXISTS
# ---------------------------------------------------------

if not EXCEL_FILE.exists():
    raise FileNotFoundError(
        f"\nExcel file not found at:\n{EXCEL_FILE}\n\n"
        "Please make sure the file is inside:\n"
        "data/raw/"
    )


# ---------------------------------------------------------
# 4. READ EXCEL WORKBOOK
# ---------------------------------------------------------

excel_file = pd.ExcelFile(EXCEL_FILE)


# ---------------------------------------------------------
# 5. DISPLAY INFORMATION
# ---------------------------------------------------------

print("=" * 60)
print("OUTLOOK CUSTOMER INTELLIGENCE PROJECT")
print("=" * 60)

print(f"\nExcel file:")
print(EXCEL_FILE)

print("\nAvailable worksheets:")

for sheet in excel_file.sheet_names:
    print(f"  - {sheet}")

print("\n" + "=" * 60)
print("EXCEL FILE CHECK COMPLETED SUCCESSFULLY")
print("=" * 60)