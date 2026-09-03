from pathlib import Path
import pandas as pd

from data_loader import load_raw_data


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
    / "data_dictionary.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

df = load_raw_data()


# =========================================================
# BUILD DATA DICTIONARY
# =========================================================

dictionary = []

for column in df.columns:

    series = df[column]

    unique_values = series.dropna().unique()

    # Convert values to strings so they can safely
    # be displayed in the data dictionary.
    sample_values = [
        str(value)
        for value in unique_values[:10]
    ]

    dictionary.append({
        "original_column": column,
        "data_type": str(series.dtype),
        "unique_count": series.nunique(dropna=True),
        "missing_count": series.isna().sum(),
        "sample_values": " | ".join(sample_values)
    })


dictionary_df = pd.DataFrame(dictionary)


# =========================================================
# DISPLAY
# =========================================================

print("=" * 100)
print("OUTLOOK CUSTOMER INTELLIGENCE")
print("DATA DICTIONARY")
print("=" * 100)

print(
    f"\nTotal columns: {len(dictionary_df)}"
)

print("\n")

print(
    dictionary_df.to_string(index=False)
)


# =========================================================
# SAVE
# =========================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

dictionary_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n" + "=" * 100)

print(
    f"Data dictionary saved to:\n{OUTPUT_PATH}"
)

print("=" * 100)