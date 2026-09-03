from pathlib import Path
import pandas as pd
import numpy as np

from data_loader import load_raw_data


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
    / "data_quality_report.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

df = load_raw_data()


print("=" * 80)
print("OUTLOOK CUSTOMER INTELLIGENCE")
print("DATA QUALITY AUDIT")
print("=" * 80)


# =========================================================
# 1. BASIC DATASET INFORMATION
# =========================================================

print("\n1. BASIC DATASET INFORMATION")
print("-" * 80)

print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]:,}")


# =========================================================
# 2. MISSING VALUE ANALYSIS
# =========================================================

print("\n2. MISSING VALUE ANALYSIS")
print("-" * 80)

missing_count = df.isna().sum()
missing_percentage = (missing_count / len(df)) * 100

total_missing = missing_count.sum()

print(f"Total missing cells : {total_missing:,}")

if total_missing == 0:
    print("Result: No missing values found.")
else:
    print("Columns containing missing values:")

    missing_table = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage.round(2)
    })

    print(
        missing_table[
            missing_table["missing_count"] > 0
        ].sort_values(
            "missing_count",
            ascending=False
        )
    )


# =========================================================
# 3. EXACT DUPLICATE ROWS
# =========================================================

print("\n3. EXACT DUPLICATE ROW ANALYSIS")
print("-" * 80)

duplicate_rows = df.duplicated().sum()

print(f"Exact duplicate rows : {duplicate_rows:,}")

if duplicate_rows == 0:
    print("Result: No exact duplicate rows found.")
else:
    print(
        f"Result: {duplicate_rows:,} exact duplicate rows found."
    )


# =========================================================
# 4. NUMERICAL COLUMN ANALYSIS
# =========================================================

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

print("\n4. NUMERICAL COLUMN SUMMARY")
print("-" * 80)

print(
    f"Numerical columns found : {len(numeric_columns)}"
)

if numeric_columns:

    numeric_summary = pd.DataFrame({
        "mean": df[numeric_columns].mean(),
        "median": df[numeric_columns].median(),
        "std": df[numeric_columns].std(),
        "min": df[numeric_columns].min(),
        "max": df[numeric_columns].max(),
        "unique_values": df[numeric_columns].nunique()
    })

    print(numeric_summary.to_string())


# =========================================================
# 5. RESPONDENT-LEVEL RESPONSE VARIATION
# =========================================================

print("\n5. RESPONDENT RESPONSE VARIATION")
print("-" * 80)

# Select survey rating columns that contain rating-style data.
# We identify columns using keywords rather than hard-coding
# a fixed list of variables.

# Identify numeric survey columns whose observed values
# are entirely within the 1-5 Likert scale.

rating_columns = []

for column in numeric_columns:

    values = df[column].dropna()

    if len(values) > 0 and values.between(1, 5).all():
        rating_columns.append(column)

print(
    f"Potential rating columns identified : "
    f"{len(rating_columns)}"
)

if rating_columns:

    rating_data = df[rating_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    respondent_unique_values = (
        rating_data.nunique(axis=1)
    )

    respondent_std = (
        rating_data.std(axis=1)
    )

    respondent_range = (
        rating_data.max(axis=1)
        - rating_data.min(axis=1)
    )

    respondent_metrics = pd.DataFrame({
        "unique_values": respondent_unique_values,
        "std": respondent_std,
        "range": respondent_range
    })

    print("\nRespondents with only ONE unique rating value:")

    one_value_count = (
        respondent_metrics["unique_values"] == 1
    ).sum()

    print(
        f"Count : {one_value_count:,}"
    )

    print(
        f"Percentage : "
        f"{one_value_count / len(df) * 100:.2f}%"
    )

    print("\nRespondent variation summary:")

    print(
        respondent_metrics.describe().to_string()
    )


# =========================================================
# 6. DUPLICATE RESPONSE PATTERNS
# =========================================================

print("\n6. DUPLICATE RESPONSE PATTERN ANALYSIS")
print("-" * 80)

if rating_columns:

    pattern_counts = (
        rating_data
        .value_counts(dropna=False)
    )

    duplicate_patterns = (
        pattern_counts[
            pattern_counts > 1
        ]
    )

    print(
        f"Unique response patterns : "
        f"{len(pattern_counts):,}"
    )

    print(
        f"Repeated response patterns : "
        f"{len(duplicate_patterns):,}"
    )

    print(
        f"Respondents belonging to repeated patterns : "
        f"{duplicate_patterns.sum():,}"
    )

    print("\nTop 10 repeated response patterns:")

    print(
        duplicate_patterns
        .head(10)
        .to_string()
    )

# =========================================================
# 7. RATING DISTRIBUTION ANALYSIS
# =========================================================

print("\n7. RATING DISTRIBUTION ANALYSIS")
print("-" * 80)

if rating_columns:

    for column in rating_columns:

        distribution = (
            df[column]
            .value_counts()
            .sort_index()
        )

        percentages = (
            df[column]
            .value_counts(normalize=True)
            .sort_index()
            * 100
        )

        print(f"\n{column}")

        distribution_table = pd.DataFrame({
            "count": distribution,
            "percentage": percentages.round(2)
        })

        print(
            distribution_table.to_string()
        )
# =========================================================
# 8. UNIFORMITY CHECK
# =========================================================

from scipy.stats import chisquare


print("\n8. UNIFORMITY CHECK")
print("-" * 80)

uniformity_results = []

for column in rating_columns:

    observed = (
        df[column]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
        .values
    )

    expected_count = len(df) / 5

    expected = np.repeat(
        expected_count,
        5
    )

    chi2_stat, p_value = chisquare(
        observed,
        f_exp=expected
    )

    uniformity_results.append({
        "column": column,
        "chi_square": chi2_stat,
        "p_value": p_value
    })

    print(f"\n{column}")
    print(f"Chi-square : {chi2_stat:.4f}")
    print(f"P-value    : {p_value:.6f}")


uniformity_df = pd.DataFrame(
    uniformity_results
)

# =========================================================
# 9. CREATE COLUMN-LEVEL QUALITY REPORT
# =========================================================

quality_report = pd.DataFrame({
    "column": df.columns,
    "data_type": df.dtypes.astype(str),
    "missing_count": df.isna().sum(),
    "missing_percentage": (
        df.isna().sum() / len(df) * 100
    ).round(2),
    "unique_values": df.nunique(
        dropna=True
    )
})


# =========================================================
# 10. SAVE REPORT
# =========================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

quality_report.to_csv(
    OUTPUT_PATH,
    index=False
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 80)
print("DATA QUALITY AUDIT SUMMARY")
print("=" * 80)

print(
    f"\nRows                  : {len(df):,}"
)

print(
    f"Columns               : {len(df.columns):,}"
)

print(
    f"Missing cells          : {total_missing:,}"
)

print(
    f"Exact duplicate rows   : {duplicate_rows:,}"
)

if rating_columns:

    print(
        f"Rating-like columns    : "
        f"{len(rating_columns):,}"
    )

    print(
        f"Straight-line rows     : "
        f"{one_value_count:,}"
    )

print(
    f"\nReport saved to:\n{OUTPUT_PATH}"
)

print("\n" + "=" * 80)
print("DATA QUALITY AUDIT COMPLETED")
print("=" * 80)