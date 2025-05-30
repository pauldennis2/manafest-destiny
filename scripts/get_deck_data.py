"""
Responsible for getting the games/deck data from the file system.
"""

import requests
import os
import pandas as pd

games_dfmap = {} # Map to orgnaize card data by set code

def leopard():
    csv_file = f"data/{set_code}/games.csv"
    df = pd.read_csv(csv_file)

    # Save as Parquet (PyArrow format)
    parquet_file = "data/bloomburrow/games.parquet"
    df.to_parquet(parquet_file, engine="pyarrow", compression="snappy")  # Snappy is fast & efficient

    print(f"Converted {csv_file} to {parquet_file}.")

    # Load the Parquet file we just created
    parquet_filestr = "data/bloomburrow/games.parquet"

    if "games_df" not in globals():
        games_df = pd.read_parquet(parquet_filestr, engine="pyarrow")
    cards_df = pd.read_csv("data/bloomburrow/cards.csv")

def convert_to_parquet(set_code: str):
    """Converts the games CSV file to Parquet format for efficient storage and retrieval."""
    csv_file = f"data/{set_code}/games.csv"
    
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file {csv_file} does not exist.")
    
    df = pd.read_csv(csv_file)

    # Save as Parquet (PyArrow format)
    parquet_file = f"data/{set_code}/games.parquet"
    df.to_parquet(parquet_file, engine="pyarrow", compression="snappy")  # Snappy is fast & efficient

    print(f"Converted {csv_file} to {parquet_file}.")
    games_dfmap[set_code] = df  # Store in the map for later use
    return df

def demo_column_efficiency():
    # Demonstrate columnar efficiency by reading only a specific column
    parquet_file = "data/blb/games.parquet"
    df = pd.read_parquet(parquet_file, columns=["draft_id"], engine="pyarrow")

    # Quick check: Print a few rows
    print(df.head())

    # Verify column type and memory usage
    print(df.info())