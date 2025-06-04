import pandas as pd

df = pd.read_csv('data/blb/games.csv', nrows=5)  # Just first 5 rows
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns[:10]}...")  # First 10 column names
print(df.head(1))  # Display the first few rows

header_df = pd.read_csv('data/blb/games.csv', nrows=0)
print(header_df.columns.tolist()[:-5])  # See first 20 column names