import pandas as pd
import argparse
import sys
import os
import math

# CONSTANTS
PROCESSED_PATH = "data/processed/movies_merged.csv"

def load_data():
    """
    Loads the processed data and prepares it for recommendation.
    Re-calculates weighted scores and explodes genres for searching.
    """
    if not os.path.exists(PROCESSED_PATH):
        print(f"Error: Data file not found at {PROCESSED_PATH}")
        print("Please run 'uv run src/ingest_data.py' first to download the dataset.")
        sys.exit(1)
        
    print("Loading data...")
    df = pd.read_csv(PROCESSED_PATH)
    
    # Data Transformation
    df['genres'] = df['genres'].str.split(',')
    df_exploded = df.explode('genres')
    
    # Calculate Weighted Score (Bayesian Average)
    C = df_exploded['averageRating'].mean()
    m = 100 # Minimum votes threshold
    
    v = df_exploded['numVotes']
    R = df_exploded['averageRating']
    
    df_exploded['weighted_score'] = (v / (v + m) * R) + (m / (v + m) * C)
    
    return df_exploded

def recommend_movie(df, genre, risk_tolerance="low", per_page=5, page=1):
    """
    Recommends movies based on genre and risk tolerance with pagination.
    """
    # 1. Filter by Genre (Case Insensitive)
    df = df.dropna(subset=['genres'])
    genre_df = df[df['genres'].str.lower() == genre.lower()].copy()
    
    if genre_df.empty:
        print(f"No movies found for genre: '{genre}'")
        return

    # 2. Apply Recommendation Strategy (Sort the entire list first)
    if risk_tolerance == "low":
        # STRATEGY: Crowd Pleasers
        rec = genre_df.sort_values(by='weighted_score', ascending=False)
    
    elif risk_tolerance == "high":
        # STRATEGY: Hidden Gems
        hidden_gems = genre_df[genre_df['numVotes'] < 5000]
        rec = hidden_gems.sort_values(by='averageRating', ascending=False)
        
    else:
        print("Invalid risk tolerance. Please use 'low' or 'high'.")
        return

    # 3. Pagination Logic
    total_results = len(rec)
    total_pages = math.ceil(total_results / per_page)
    
    if page < 1:
        page = 1
        
    if page > total_pages and total_results > 0:
        print(f"Page {page} is out of range. There are only {total_pages} pages.")
        return

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    
    # Slice the dataframe for the specific page
    page_results = rec.iloc[start_index:end_index]

    # 4. Display Results
    print(f"\n--- RECOMMENDATIONS FOR '{genre.upper()}' ({risk_tolerance.upper()} RISK) ---")
    print(f"--- Page {page} of {total_pages} ({total_results} movies found) ---")
    
    clean_results = page_results[['primaryTitle', 'startYear', 'averageRating', 'numVotes', 'weighted_score']]
    print(clean_results.to_string(index=False))

def main():
    parser = argparse.ArgumentParser(description="Movie Recommender Tool")
    
    parser.add_argument(
        "--genre", 
        type=str, 
        required=True, 
        help="The genre you want to watch (e.g., Action, Horror, Comedy)"
    )
    
    parser.add_argument(
        "--risk", 
        type=str, 
        choices=['low', 'high'], 
        default='low', 
        help="Risk tolerance: 'low' for blockbusters, 'high' for hidden gems"
    )
    
    parser.add_argument(
        "-n", 
        type=int, 
        default=5, 
        help="Number of movies per page"
    )

    # NEW ARGUMENT
    parser.add_argument(
        "--page", 
        type=int, 
        default=1, 
        help="The page number to view"
    )

    args = parser.parse_args()

    # Execute
    df = load_data()
    # Pass 'n' as 'per_page' and 'page' as the page number
    recommend_movie(df, args.genre, args.risk, args.n, args.page)

if __name__ == "__main__":
    main()