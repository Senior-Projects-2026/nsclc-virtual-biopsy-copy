"""Generates a report and bar chart showing the distribution of positive and negative EGFR labels."""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "processed" / "patients.csv"
OUTPUT_DIR = ROOT / "reports" / "figures"


def generate_report():
    dataset = pd.read_csv(DATASET_PATH)

    counts = dataset["egfr_label"].value_counts()

    print("EGFR distribution:")
    print(counts)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    counts.plot(kind="bar", title="EGFR Label Distribution")
    plt.xlabel("EGFR Label")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "egfr_distribution.png")
    plt.close()


if __name__ == "__main__":
    generate_report()
