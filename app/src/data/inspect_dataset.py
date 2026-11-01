from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"

FILES = [
    "egfr_per_patient.csv",
    "patients.csv",
    "imaging_studies.csv",
]

for filename in FILES:
    path = RAW_DIR / filename

    print(f"\n{'=' * 60}")
    print(filename)
    print("=" * 60)

    if not path.exists():
        print("File not found!")
        continue

    df = pd.read_csv(path)

    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head().to_string())
    print("\nMissing values:")
    print(df.isnull().sum())

    #what imaging tech was used to insepct
    if filename == "imaging_studies.csv":
        print("\nModality values:")
        print(df["modalities"].value_counts(dropna=False))