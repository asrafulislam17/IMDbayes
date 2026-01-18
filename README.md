# IMDb Movie Genre Analysis

## Project Overview
This project analyzes **IMDb dataset** (movies > 100 votes) to determine how different genres perform in terms of ratings and audience reception. We specifically look at the "Masterpiece Gap"—the difference between an average movie in a genre and the top 1% (p99).

## Key Findings
* **The "Safe" Genres:** Documentaries and Biographies have the highest average ratings (>7.0), suggesting a selection bias in their audience.
* **The "Risk" Genres:** Horror and Sci-Fi have the lowest averages (<5.5) but maintain high p99 ceilings. This indicates a "Hit or Miss" market where execution quality varies wildly.
* **The Animation Anomaly:** Animation consistently performs well in both average and elite tiers.

## Methodology
1. **Ingestion:** Streamed raw `title.basics` and `title.ratings` from IMDb interfaces.
2. **Cleaning:** Filtered for movies with >100 votes to remove noise (Power Law distribution).
3. **Metric Engineering:** Calculated **Weighted Ratings** using the Bayesian Average formula to penalize low-volume outliers.
4. **Quantiles:** Used `p99` (99th percentile) to model the "ceiling" of every genre.

## Tech Stack
* **Python 3.10**
* **Pandas** (Data Manipulation)
* **Seaborn** (Visualization)
* **uv** (Package Management)

## How to Run
1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Sync dependencies: `uv sync`
3. Download data: `uv run src/ingest_data.py`
4. Explore: Open `notebooks/1_exploration.ipynb`