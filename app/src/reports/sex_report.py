from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "processed" / "patients.csv"
OUTPUT_DIR = ROOT / "reports" / "figures"


def generate_report():
    dataset = pd.read_csv(DATASET_PATH)

    # Comment lines 16 for women vs men, and comment line 15 for women vs men vs unkown
    # counts = dataset["sex"].fillna("Unknown").value_counts()
    counts = dataset["sex"].dropna().value_counts()

    print("Sex distribution:")
    print(counts)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    counts.plot(kind="bar", title="Patient Sex Distribution")
    plt.xlabel("Sex")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sex_distribution.png")
    plt.close()


if __name__ == "__main__":
    generate_report()
