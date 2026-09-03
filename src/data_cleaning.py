from pathlib import Path
import re
import pandas as pd
import numpy as np

from data_loader import load_raw_data


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_survey.csv"
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_column_name(column_name):
    """
    Convert a raw survey question into a readable snake_case
    column name.

    Example:
    'What is your gender?' -> 'what_is_your_gender'
    """

    name = str(column_name).strip().lower()

    # Replace common symbols with words/spaces
    name = name.replace("&", "and")
    name = name.replace("/", " ")
    name = name.replace("'", "")

    # Keep only letters, numbers and spaces
    name = re.sub(r"[^a-z0-9]+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    return name


def make_unique_column_names(columns):
    """
    Ensure that cleaned column names are unique.
    """

    counts = {}
    unique_columns = []

    for column in columns:

        if column not in counts:
            counts[column] = 0
            unique_columns.append(column)

        else:
            counts[column] += 1
            unique_columns.append(
                f"{column}_{counts[column]}"
            )

    return unique_columns


def find_column(df, phrase, occurrence=0):
    """
    Find a column using a phrase contained in its name.

    occurrence=0 means first matching column.
    occurrence=1 means second matching column.
    """

    matches = [
        column
        for column in df.columns
        if phrase.lower() in str(column).strip().lower()
    ]

    if len(matches) <= occurrence:
        raise KeyError(
            f"Could not find occurrence {occurrence} "
            f"of column containing:\n{phrase}"
        )

    return matches[occurrence]


# =========================================================
# LOAD RAW DATA
# =========================================================

print("=" * 80)
print("OUTLOOK CUSTOMER INTELLIGENCE")
print("DATA CLEANING & FEATURE ENGINEERING")
print("=" * 80)

df = load_raw_data()

print(
    f"\nRaw dataset shape: {df.shape}"
)


# =========================================================
# 1. STANDARDIZE TEXT VALUES
# =========================================================

print("\n1. STANDARDIZING TEXT VALUES")
print("-" * 80)

text_columns = df.select_dtypes(
    include="object"
).columns

for column in text_columns:

    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )


# =========================================================
# 2. CORRECT OBVIOUS TYPOGRAPHICAL INCONSISTENCIES
# =========================================================

print("\n2. CORRECTING KNOWN TEXT INCONSISTENCIES")
print("-" * 80)

text_replacements = {
    "Linkedln": "LinkedIn",
    "Linkedin": "LinkedIn",
    "Reliablity": "Reliability",
    "Quaterly": "Quarterly",
    "Sophitication": "Sophistication",
    "Competance": "Competence",
    "70 above": "70+",
}

replacement_count = 0

for column in text_columns:

    before = df[column].copy()

    df[column] = df[column].replace(
        text_replacements
    )

    replacement_count += (
        before != df[column]
    ).sum()

print(
    f"Text values standardized: "
    f"{replacement_count:,}"
)


# =========================================================
# 3. IDENTIFY IMPORTANT BUSINESS VARIABLES
# =========================================================

print("\n3. IDENTIFYING BUSINESS VARIABLES")
print("-" * 80)


# -------------------------
# DEMOGRAPHICS
# -------------------------

age_col = find_column(
    df,
    "In which age bracket do you fall?"
)

gender_col = find_column(
    df,
    "What is your gender?"
)

education_col = find_column(
    df,
    "What is your education level?"
)

location_col = find_column(
    df,
    "Where do you live?"
)

employment_col = find_column(
    df,
    "What is your employment status?"
)


# -------------------------
# AWARENESS
# -------------------------

awareness_col_1 = find_column(
    df,
    "Are you aware of Outlook magazine?",
    occurrence=0
)

awareness_col_2 = find_column(
    df,
    "Are you aware of Outlook magazine?",
    occurrence=1
)

familiarity_col = find_column(
    df,
    "How familiar are you with Outlook magazine?"
)


# -------------------------
# MARKETING
# -------------------------

discovery_col = find_column(
    df,
    "How do you come to know about the magazine brand"
)

awareness_driver_col = find_column(
    df,
    "What influences the brand awareness the most?"
)

ad_platform_col = find_column(
    df,
    "Where do you do your magic and run digital ad campaigns?"
)

campaign_frequency_col = find_column(
    df,
    "How frequently do you (or your organization) run digital ads"
)

digital_buy_frequency_col = find_column(
    df,
    "How often do you buy products using digital channels?"
)

digital_spend_col = find_column(
    df,
    "How much would you like to spend on the products from Digital channels"
)


# -------------------------
# LOYALTY / REPURCHASE
# -------------------------

previous_purchase_col = find_column(
    df,
    "Have you previously purchased/used our service/product?"
)

recommendation_col = find_column(
    df,
    "On a scale of 5 how likely is it for you to recommend"
)

repurchase_col = find_column(
    df,
    "Would you consider buying again?"
)

magazine_repurchase_col = find_column(
    df,
    "Would you buy Outlook magazine again?"
)


# -------------------------
# CUSTOMER EXPERIENCE
# -------------------------

life_improvement_col = find_column(
    df,
    "On a scale of 5 how much our product or service improve your life?"
)

service_col = find_column(
    df,
    "rate us on our 'Service'"
)

content_col = find_column(
    df,
    "rate us on our 'Content'"
)

price_col = find_column(
    df,
    "rate us on our 'Price'"
)

delivery_col = find_column(
    df,
    "rate us on our 'Delivery'"
)

experience_col = find_column(
    df,
    "rate your previous Experience with us"
)

solution_col = find_column(
    df,
    "How do you feel about our brand as a solution?"
)

support_col = find_column(
    df,
    "How helpful was our customer support team?"
)

overall_rating_col = find_column(
    df,
    "How would you rate Outlook magazine overall?"
)

overall_experience_col = find_column(
    df,
    "How would you rate your experience overall?"
)


# =========================================================
# 4. CREATE CLEAN BUSINESS-FRIENDLY COLUMN NAMES
# =========================================================

print("\n4. CREATING CLEAN COLUMN NAMES")
print("-" * 80)

rename_map = {

    age_col: "age_group",
    gender_col: "gender",
    education_col: "education_level",
    location_col: "residence_type",
    employment_col: "employment_status",

    awareness_col_1: "outlook_awareness_1",
    awareness_col_2: "outlook_awareness_2",
    familiarity_col: "outlook_familiarity",

    discovery_col: "brand_discovery_method",
    awareness_driver_col: "brand_awareness_driver",
    ad_platform_col: "digital_ad_platform",
    campaign_frequency_col: "digital_campaign_frequency",
    digital_buy_frequency_col: "digital_purchase_frequency",
    digital_spend_col: "digital_monthly_spend",

    previous_purchase_col: "previous_purchase",
    recommendation_col: "recommendation",
    repurchase_col: "repurchase_intent",
    magazine_repurchase_col: "magazine_repurchase_intent",

    life_improvement_col: "life_improvement_rating",
    service_col: "service_rating",
    content_col: "content_rating",
    price_col: "price_rating",
    delivery_col: "delivery_rating",
    experience_col: "previous_experience_rating",
    solution_col: "brand_solution_rating",
    support_col: "customer_support_rating",
    overall_rating_col: "overall_magazine_rating",
    overall_experience_col: "overall_experience_rating",
}


# First clean all columns generically
cleaned_names = [
    clean_column_name(column)
    for column in df.columns
]

cleaned_names = make_unique_column_names(
    cleaned_names
)

df.columns = cleaned_names


# Create a mapping from original columns to cleaned
# generic names so we can apply the business names.
original_columns = list(
    load_raw_data().columns
)

generic_mapping = dict(
    zip(
        original_columns,
        cleaned_names
    )
)

# Translate raw business-column names into their
# corresponding generic cleaned names.
final_rename_map = {}

for raw_column, business_name in rename_map.items():

    generic_name = generic_mapping[raw_column]

    final_rename_map[
        generic_name
    ] = business_name


df = df.rename(
    columns=final_rename_map
)


print(
    f"Total columns after cleaning: "
    f"{len(df.columns)}"
)


# =========================================================
# 5. CONVERT RATING VARIABLES TO NUMERIC
# =========================================================

print("\n5. VALIDATING RATING VARIABLES")
print("-" * 80)

rating_columns = [
    "recommendation",
    "life_improvement_rating",
    "service_rating",
    "content_rating",
    "price_rating",
    "delivery_rating",
    "previous_experience_rating",
    "outlook_familiarity",
    "brand_solution_rating",
    "customer_support_rating",
    "overall_magazine_rating",
    "overall_experience_rating",
]

for column in rating_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid_values = (
        ~df[column].between(1, 5)
    ).sum()

    if invalid_values > 0:

        raise ValueError(
            f"{column} contains "
            f"{invalid_values} invalid values."
        )


print(
    "All 12 rating variables validated "
    "successfully on the 1–5 scale."
)


# =========================================================
# 6. AWARENESS CONSISTENCY
# =========================================================

print("\n6. CREATING AWARENESS CONSISTENCY FEATURES")
print("-" * 80)

df["awareness_consistent"] = (
    df["outlook_awareness_1"].str.lower()
    ==
    df["outlook_awareness_2"].str.lower()
)

df["awareness_disagreement"] = (
    ~df["awareness_consistent"]
).astype(int)

agreement_rate = (
    df["awareness_consistent"].mean()
    * 100
)

print(
    f"Awareness agreement: "
    f"{agreement_rate:.2f}%"
)

print(
    f"Awareness disagreements: "
    f"{df['awareness_disagreement'].sum():,}"
)


# =========================================================
# 7. RECOMMENDATION CATEGORY
# =========================================================

print("\n7. CREATING RECOMMENDATION SEGMENTS")
print("-" * 80)

df["recommendation_category"] = pd.cut(
    df["recommendation"],
    bins=[0, 2, 3, 5],
    labels=[
        "Detractor",
        "Passive",
        "Promoter"
    ],
    include_lowest=True
)

print(
    df["recommendation_category"]
    .value_counts()
    .sort_index()
)


# =========================================================
# 8. REPURCHASE INTENT SCORE
# =========================================================

print("\n8. CREATING REPURCHASE INTENT SCORE")
print("-" * 80)

repurchase_mapping = {
    "No": 1,
    "Will think of it": 2,
    "Yes": 3
}

df["repurchase_intent_score"] = (
    df["repurchase_intent"]
    .map(repurchase_mapping)
)

unmapped_repurchase = (
    df["repurchase_intent_score"].isna().sum()
)

if unmapped_repurchase > 0:

    raise ValueError(
        "Some repurchase-intent values could not "
        "be mapped."
    )

print(
    "Repurchase intent successfully converted "
    "to an ordinal 1–3 score."
)


# =========================================================
# 9. RESPONDENT-LEVEL RATING FEATURES
# =========================================================

print("\n9. CREATING RESPONDENT-LEVEL RATING FEATURES")
print("-" * 80)

rating_data = df[rating_columns]

df["rating_mean"] = (
    rating_data.mean(axis=1)
)

df["rating_std"] = (
    rating_data.std(axis=1)
)

df["rating_range"] = (
    rating_data.max(axis=1)
    - rating_data.min(axis=1)
)

df["rating_unique_count"] = (
    rating_data.nunique(axis=1)
)


# =========================================================
# 10. DATA QUALITY FLAG
# =========================================================

df["potential_low_variation_response"] = (
    df["rating_unique_count"] <= 2
)


print(
    "Respondent-level variation features created."
)


# =========================================================
# 11. FINAL VALIDATION
# =========================================================

print("\n11. FINAL DATA VALIDATION")
print("-" * 80)

print(
    f"Rows    : {df.shape[0]:,}"
)

print(
    f"Columns : {df.shape[1]:,}"
)

print(
    f"Missing cells : "
    f"{df.isna().sum().sum():,}"
)

print(
    f"Duplicate rows : "
    f"{df.duplicated().sum():,}"
)


if df.isna().sum().sum() != 0:

    raise ValueError(
        "Unexpected missing values were introduced "
        "during cleaning."
    )


# =========================================================
# 12. SAVE CLEAN DATASET
# =========================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 80)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 80)

print(
    f"\nCleaned dataset saved to:\n"
    f"{OUTPUT_PATH}"
)

print(
    f"\nFinal shape: "
    f"{df.shape[0]:,} rows × "
    f"{df.shape[1]:,} columns"
)

print("\nKey analytical variables:")

for column in [
    "outlook_awareness_1",
    "outlook_awareness_2",
    "outlook_familiarity",
    "recommendation",
    "recommendation_category",
    "repurchase_intent",
    "repurchase_intent_score",
    "service_rating",
    "content_rating",
    "price_rating",
    "delivery_rating",
    "previous_experience_rating",
    "customer_support_rating",
]:
    print(f"  - {column}")

print("\n" + "=" * 80)
