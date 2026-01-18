import pandas as pd
import gzip
import shutil
import os

# CONSTANTS
# IMDb uses tsv (Tab Separated Values) and 'gzip' compression
BASICS_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"
RATINGS_URL = "https://datasets.imdbws.com/title.ratings.tsv.gz"

# Paths
RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed/movies_merged.csv"

def load_basics():
    """
    Loads title.basics. 
    STRATEGY: This file is huge (millions of rows). 
    We filter immediately to keep only 'movie' types to save RAM.
    """
    print(f"Downloading and streaming {BASICS_URL}...")
    
    # Chunksize allows us to process the file in parts if it's too big, 
    # but for a modern laptop, reading strictly 'movie' types is manageable.
    # We use 'na_values' because IMDb uses '\N' to denote missing data.
    df = pd.read_csv(
        BASICS_URL, 
        sep='\t', 
        encoding='utf-8', 
        na_values='\\N', 
        usecols=['tconst', 'titleType', 'primaryTitle', 'startYear', 'genres'],
        dtype={'startYear': 'Int64'} # Handle years as nullable integers
    )
    
    # FILTER 1: Only Movies (exclude TV episodes, shorts, etc.)
    print(f"Raw titles count: {len(df)}")
    df = df[df['titleType'] == 'movie']
    
    # FILTER 2: Modern Era (Optional, but let's stick to 1980+ for better data quality)
    df = df[df['startYear'] >= 1980]
    
    print(f"Filtered movie count: {len(df)}")
    return df

def load_ratings():
    """
    Loads title.ratings.
    """
    print(f"Downloading and streaming {RATINGS_URL}...")
    df = pd.read_csv(
        RATINGS_URL, 
        sep='\t', 
        encoding='utf-8', 
        na_values='\\N',
        dtype={'averageRating': float, 'numVotes': int}
    )
    return df

def main():
    # 1. Load Data
    basics_df = load_basics()
    ratings_df = load_ratings()
    
    # 2. Merge (The "Join" Operation)
    # We join on 'tconst' (the unique IMDb ID, e.g., tt0111161)
    print("Merging datasets...")
    merged_df = pd.merge(basics_df, ratings_df, on='tconst', how='inner')
    
    # 3. Clean Genres
    # Drop movies with no genre defined
    merged_df = merged_df.dropna(subset=['genres'])
    
    # 4. Save to Disk
    # We save as CSV for easy inspection later
    print(f"Saving {len(merged_df)} rows to {PROCESSED_PATH}...")
    merged_df.to_csv(PROCESSED_PATH, index=False)
    print("Done! Environment is primed.")

if __name__ == "__main__":
    main()