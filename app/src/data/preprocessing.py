"""Joins and filters the patient, EGFR, and imaging datasets to produce the eligible training and validation datasets and DICOM folder list."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports" / "figures"


def load_data():
    egfr = pd.read_csv(RAW_DIR / "egfr_per_patient.csv")
    patients = pd.read_csv(RAW_DIR / "patients.csv")
    imaging = pd.read_csv(RAW_DIR / "imaging_studies.csv")

    return egfr, patients, imaging


def preprocess():
    egfr, patients, imaging = load_data()

    # Keep only train and validation patients
    patients = patients[patients["split"].isin(["train", "val"])].copy()

    # Keep only patients with a valid EGFR label
    egfr = egfr[egfr["egfr_label"].isin(["positive", "negative"])].copy()

    # Keep only patients with available imaging
    patients = patients[patients["has_imaging"] == 1]

    # Join patients with EGFR labels
    dataset = patients.merge(egfr, on="patient_key", how="inner")

    # Join patients with their imaging studies
    imaging = imaging[["patient_key", "anon_id", "modalities", ""]].drop_duplicates()

    dataset = dataset.merge(imaging, on="patient_key", how="inner")

    # Keep only CT studies
    dataset = dataset[
        dataset["modalities"].fillna("").str.contains(r"\bCT\b", case=False, regex=True)
    ].copy()

    # Remove patients without a CT study
    dataset = dataset.dropna(subset=["anon_id"])

    # Preserve conflict information; do not silently discard conflicts
    dataset["egfr_conflict"] = dataset["egfr_conflict"].fillna(False)

    # Export one patient-level row per patient
    patient_dataset = dataset.drop_duplicates("patient_key")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    patient_dataset.to_csv(PROCESSED_DIR / "patients.csv", index=False)

    # Export train and validation datasets
    patient_dataset[patient_dataset["split"] == "train"].to_csv(
        PROCESSED_DIR / "train.csv", index=False
    )

    patient_dataset[patient_dataset["split"] == "val"].to_csv(
        PROCESSED_DIR / "val.csv", index=False
    )

    # Export unique DICOM archive folder identifiers
    anon_ids = sorted(dataset["anon_id"].dropna().unique())

    (PROCESSED_DIR / "dicom_folders.txt").write_text(
        "\n".join(anon_ids) + "\n"
    )

    print("\nDataset summary")
    print("=" * 40)
    print(f"Eligible patients: {patient_dataset['patient_key'].nunique()}")
    print(f"Training patients: {(patient_dataset['split'] == 'train').sum()}")
    print(f"Validation patients: {(patient_dataset['split'] == 'val').sum()}")
    print(f"Positive EGFR: {(patient_dataset['egfr_label'] == 'positive').sum()}")
    print(f"Negative EGFR: {(patient_dataset['egfr_label'] == 'negative').sum()}")
    print(f"Conflicting EGFR: {patient_dataset['egfr_conflict'].sum()}")
    print(f"Unique DICOM folders: {len(anon_ids)}")

if __name__ == "__main__":
    preprocess()
