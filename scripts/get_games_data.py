"""
Responsible for getting the games/deck data from the file system.
"""

import os
import pandas as pd

games_dfmap = {} # Map to orgnaize card data by set code

def get_games_data(set_code: str):
    """Retrieves games data, prioritizing cached data, then Parquet, and finally CSV."""
    if set_code in games_dfmap:
        return games_dfmap[set_code]

    parquet_file = f"data/{set_code}/games.parquet"
    csv_file = f"data/{set_code}/games.csv"

    if os.path.exists(parquet_file):
        print(f"Loading game data for {set_code} from Parquet file...")
        df = pd.read_parquet(parquet_file, engine="pyarrow")
        games_dfmap[set_code] = df
        return df

    if os.path.exists(csv_file):
        print(f"Reading and converting data for {set_code} to Parquet...")
        df = convert_to_parquet_(set_code)
        games_dfmap[set_code] = df
        return df
    
def convert_to_parquet_(set_code: str):
    """Converts the games CSV file to Parquet format for efficient storage and retrieval."""
    csv_file = f"data/{set_code}/games.csv"
    parquet_file = f"data/{set_code}/games.parquet"

    if os.path.exists(parquet_file):
        print(f"Parquet file {parquet_file} already exists. No conversion needed.")
        return games_dfmap.get(set_code, pd.read_parquet(parquet_file, engine="pyarrow"))

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file {csv_file} does not exist.")

    df = pd.read_csv(csv_file)
    df.to_parquet(parquet_file, engine="pyarrow", compression="snappy")  # Snappy is fast & efficient
    print(f"Converted {csv_file} to {parquet_file}.")
    
    games_dfmap[set_code] = df
    return df

def demo_column_efficiency():
    # Demonstrate columnar efficiency by reading only a specific column
    parquet_file = "data/blb/games.parquet"
    df = pd.read_parquet(parquet_file, columns=["draft_id"], engine="pyarrow")

    # Quick check: Print a few rows
    print(df.head())

    # Verify column type and memory usage
    print(df.info())