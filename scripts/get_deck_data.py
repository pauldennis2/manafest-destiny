"""
Responsible for getting the deck data from the API and saving it to a file.

Cleaning included free of charge.
"""
import requests
import os
import pandas as pd

def demo_column_efficiency():
    # Demonstrate columnar efficiency by reading only a specific column
    parquet_file = "data/blb/games.parquet"
    df = pd.read_parquet(parquet_file, columns=["draft_id"], engine="pyarrow")

    # Quick check: Print a few rows
    print(df.head())

    # Verify column type and memory usage
    print(df.info())