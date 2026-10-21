"""
data/generate_dataset.py
Generates a realistic synthetic student placement dataset (500 records).

The target label (placed) is derived from a logistic probability function
based on all features — no arbitrary thresholds or fabricated accuracy.
Run once:  python data/generate_dataset.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
N = 600


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generate() -> pd.DataFrame:
    cgpa = RNG.uniform(5.0, 10.0, N).round(2)
    aptitude_score = RNG.integers(30, 101, N).astype(float)
    num_projects = RNG.integers(0, 9, N).astype(float)
    num_internships = RNG.integers(0, 4, N).astype(float)
    num_certifications = RNG.integers(0, 11, N).astype(float)
    num_workshops = RNG.integers(0, 6, N).astype(float)
    communication_skills = RNG.integers(1, 6, N).astype(float)  # 1–5 Likert
    technical_skills_score = RNG.integers(30, 101, N).astype(float)
    backlogs = RNG.choice([0, 0, 0, 1, 2, 3], size=N).astype(float)  # skewed toward 0

    # Logistic score — weighted combination of features
    score = (
        0.55 * (cgpa - 7.5)
        + 0.035 * (aptitude_score - 65)
        + 0.30 * num_projects
        + 0.50 * num_internships
        + 0.12 * num_certifications
        + 0.08 * num_workshops
        + 0.18 * (communication_skills - 3)
        + 0.030 * (technical_skills_score - 65)
        - 0.60 * backlogs
        + RNG.normal(0, 0.4, N)  # realistic noise
    )

    prob = sigmoid(score)
    placed = RNG.binomial(1, prob).astype(int)

    df = pd.DataFrame({
        "cgpa": cgpa,
        "aptitude_score": aptitude_score.astype(int),
        "num_projects": num_projects.astype(int),
        "num_internships": num_internships.astype(int),
        "num_certifications": num_certifications.astype(int),
        "num_workshops": num_workshops.astype(int),
        "communication_skills": communication_skills.astype(int),
        "technical_skills_score": technical_skills_score.astype(int),
        "backlogs": backlogs.astype(int),
        "placed": placed,
    })

    return df


if __name__ == "__main__":
    out = Path(__file__).parent / "dataset.csv"
    df = generate()
    df.to_csv(out, index=False)
    placed_pct = df["placed"].mean() * 100
    print(f"[OK]  Dataset saved to {out}")
    print(f"   Records : {len(df)}")
    print(f"   Placed  : {placed_pct:.1f}%  |  Not Placed: {100 - placed_pct:.1f}%")
    print(df.describe().to_string())
