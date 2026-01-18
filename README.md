## [Read the Related Blogpost](https://fezcode.com/blog/what-genre-should-i-watch?theme=editorial)

# IMDbayes (_"I'm Da Bayes"_) : IMDb Genre Gap Analysis & Recommender
> _I love it when you call me Big Data._

![IMDBayes Banner](./imdbayes.png)

A Data Science project analyzing the "Masterpiece Gap", the statistical difference between an average movie and the top 1% (p99) across different genres.

## Project Overview
As software engineers, we often look at averages, but averages lie. If a genre has a polarizing audience (half 1/10, half 10/10), the average is 5/10—same as a "boring" genre.

This project uses **Python**, **Pandas**, and **Bayesian Statistics** to:
1.  **Ingest & Clean** raw IMDb datasets (streaming >200MB of data).
2.  **Analyze** the risk/reward profile of every major film genre.
3.  **Recommend** movies using a CLI tool with adjustable "Risk Tolerance" profiles.

## Key Findings (The Data Science)
Our analysis revealed distinct "personalities" for each genre:
* **The Safe Bets (Documentary, Biography):** These have high averages and low variance. It is statistically difficult to make a "bad" documentary.
* **The High-Risk/High-Reward (Horror, Sci-Fi):** These have the lowest average ratings, but their **p99 (Top 1%)** ceiling is as high as Drama. This huge "gap" implies execution difficulty.
* **The Animation Anomaly:** The only genre that consistently maintains both a high floor (average) and a high ceiling (p99).

## Methodology & Metrics

### 1. The Weighted Rating (Bayesian Average)
To prevent movies with 5 votes from skewing the data, we use the official IMDb formula. This penalizes low-volume outliers and pulls them toward the global mean.

$$
WR = \left( \frac{v}{v+m} \cdot R \right) + \left( \frac{m}{v+m} \cdot C \right)
$$

**Where:**
* $R$ = Average Rating of the movie
* $v$ = Number of votes for the movie
* $m$ = Minimum votes required to be listed (Threshold: 100)
* $C$ = Mean vote across the whole dataset

### 2. The p99 (99th Percentile)
We calculate the 99th percentile rating for each genre. This represents the "Masterpiece Ceiling"—the maximum potential quality a genre typically achieves.

---

## Tech Stack & Prerequisites
We use **`uv`**, a blazing-fast Python package manager written in Rust, to handle dependencies and environments.

* **Language:** Python 3.10+
* **Manager:** `uv` (replaces pip/conda)
* **Libraries:** Pandas, Seaborn, Matplotlib, Scipy

### Prerequisites
You only need to install `uv`. It will handle Python and all libraries for you.

**Mac / Linux:**
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

```

**Windows (PowerShell):**

```powershell
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

```

---

## How to Run (Step-by-Step)

### Step 1: Initialize & Install

Clone the repo and sync the dependencies. `uv` will create a virtual environment (`.venv`) automatically.

```bash
# 1. Sync dependencies
uv sync

```

### Step 2: Data Ingestion (CRITICAL)

**You must run this script first.**
The repository does **not** contain the dataset (it is ignored via `.gitignore`). You need to stream the data from IMDb, clean it, and build the local cache.

```bash
# Downloads title.basics and title.ratings, merges them, and filters for movies
uv run src/ingest_data.py

```

*Output: Creates `data/processed/movies_merged.csv` (~50-100MB)*

### Step 3: View the Analysis

To see the boxplots, gap analysis charts, and statistical breakdown, open the Jupyter Notebook.

* Open VS Code.
* Open `notebooks/1_exploration.ipynb`.
* Select the Kernel: `Python Environments` -> `.venv`.
* Run All Cells.

### Step 4: Use the CLI Recommender

We built a custom CLI tool to recommend movies based on the statistical findings.

**Option A: Low Risk (Crowd Pleasers)**
Finds movies with high **Weighted Ratings**. Safe bets.

```bash
uv run src/recommender.py --genre "Sci-Fi" --risk low

```

**Option B: High Risk (Hidden Gems)**
Finds movies with high **Raw Ratings** but lower vote counts (< 5000). Good for finding cult classics.

```bash
uv run src/recommender.py --genre "Horror" --risk high

```

**Option C: Pagination**
Browse through the results.

```bash
uv run src/recommender.py --genre "Comedy" --page 2 -n 10

```

---

## Project Structure

```text
IMDbayes/
├── data/
│   ├── raw/             # Temp folder for downloads (ignored)
│   └── processed/       # The final CSV used by the app (ignored)
├── notebooks/
│   └── 1_exploration.ipynb  # The Data Science Lab (Charts & Analysis)
├── src/
│   ├── ingest_data.py   # ETL Script (Download -> Clean -> Save)
│   └── recommender.py   # CLI Application Logic
├── .gitignore           # Ensures data is never committed
├── pyproject.toml       # Dependencies managed by uv
└── README.md            # This file
```
