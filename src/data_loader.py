from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "outlook_consumer_survey.xlsx"
)


# ---------------------------------------------------------
# DATA LOADING FUNCTION
# ---------------------------------------------------------

def load_raw_data(
    file_path: Path = RAW_DATA_PATH
) -> pd.DataFrame:
    """
    Load the raw Outlook consumer survey dataset.

    Parameters
    ----------
    file_path : Path
        Location of the Excel workbook.

    Returns
    -------
    pd.DataFrame
        Raw survey dataset.
    """

    # Check that the file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"\nDataset not found at:\n{file_path}\n\n"
            "Please make sure the Excel file is located inside "
            "data/raw/."
        )

    # Load the Data 1 worksheet
    df = pd.read_excel(
        file_path,
        sheet_name="Data 1"
    )

    return df


# ---------------------------------------------------------
# TEST THE DATA LOADER
# ---------------------------------------------------------

if __name__ == "__main__":

    df = load_raw_data()

    print("=" * 60)
    print("OUTLOOK CUSTOMER INTELLIGENCE")
    print("=" * 60)

    print(f"\nDataset successfully loaded.")

    print(f"\nNumber of rows    : {df.shape[0]:,}")
    print(f"Number of columns : {df.shape[1]:,}")

    print("\nColumn names:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\n" + "=" * 60)
    print("DATA LOADING COMPLETED SUCCESSFULLY")
    print("=" * 60)