from pathlib import Path
import subprocess
import sys


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


# =========================================================
# HELPER FUNCTION
# =========================================================

def run_script(script_name):
    """
    Run a Python script located inside the src folder.
    Stop the pipeline if the script fails.
    """

    script_path = SRC_DIR / script_name

    print("\n" + "=" * 70)
    print(f"RUNNING: {script_name}")
    print("=" * 70)

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script not found:\n{script_path}"
        )

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"\nPipeline stopped because {script_name} failed."
        )

    print(f"\n{script_name} completed successfully.")


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():

    print("=" * 70)
    print("OUTLOOK CUSTOMER INTELLIGENCE PIPELINE")
    print("=" * 70)

    # Step 1: Check raw Excel file
    run_script("check_excel.py")

    # Step 2: Run data cleaning and feature engineering
    run_script("data_cleaning.py")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()