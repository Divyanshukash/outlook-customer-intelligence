from pathlib import Path
import pandas as pd

from data_loader import load_raw_data


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
    / "variable_inventory.csv"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_raw_data()


# ---------------------------------------------------------
# CREATE VARIABLE INVENTORY
# ---------------------------------------------------------

inventory = []

for column in df.columns:

    series = df[column]

    # Number of missing values
    missing_count = series.isna().sum()

    # Missing percentage
    missing_percentage = (
        missing_count / len(df)
    ) * 100

    # Number of unique values
    unique_count = series.nunique(dropna=True)

    # Data type
    data_type = str(series.dtype)

    # Example values
    example_values = (
        series.dropna()
        .astype(str)
        .drop_duplicates()
        .head(5)
        .tolist()
    )

    inventory.append({
        "column": column,
        "data_type": data_type,
        "unique_values": unique_count,
        "missing_values": missing_count,
        "missing_percentage": round(missing_percentage, 2),
        "example_values": " | ".join(example_values)
    })


# ---------------------------------------------------------
# CONVERT TO DATAFRAME
# ---------------------------------------------------------

inventory_df = pd.DataFrame(inventory)


# ---------------------------------------------------------
# DISPLAY INVENTORY
# ---------------------------------------------------------

print("=" * 80)
print("OUTLOOK CUSTOMER INTELLIGENCE")
print("VARIABLE INVENTORY")
print("=" * 80)

print(f"\nTotal rows    : {len(df):,}")
print(f"Total columns : {len(df.columns):,}")

print("\nVariable inventory:\n")

print(
    inventory_df.to_string(index=False)
)


# ---------------------------------------------------------
# SAVE INVENTORY
# ---------------------------------------------------------

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

inventory_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(
    f"\nTotal variables : {len(df.columns)}"
)

print(
    f"Numerical variables : "
    f"{df.select_dtypes(include='number').shape[1]}"
)

print(
    f"Non-numerical variables : "
    f"{df.select_dtypes(exclude='number').shape[1]}"
)

print(
    f"Total missing values : "
    f"{df.isna().sum().sum():,}"
)

print(
    f"Exact duplicate rows : "
    f"{df.duplicated().sum():,}"
)

print(
    f"\nInventory saved to:\n{OUTPUT_PATH}"
)

print("\n" + "=" * 80)
print("VARIABLE INVENTORY COMPLETED SUCCESSFULLY")
print("=" * 80)
