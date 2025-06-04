import os
import pandas as pd
import psutil
import pyarrow.csv as pv

# Map to organize card data by set code
games_dfmap = {}

def get_games_data(set_code: str):
    """
    Retrieves games data, prioritizing cached data, then Feather, and finally CSV.

    Args:
        set_code (str): The code for the game set (e.g., 'MKM').

    Returns:
        pd.DataFrame: The DataFrame containing the game data for the specified set.

    Raises:
        FileNotFoundError: If no data (Feather or CSV) is found for the set.
    """
    if set_code in games_dfmap:
        return games_dfmap[set_code]

    feather_file = f"data/{set_code}/games.feather"
    csv_file = f"data/{set_code}/games.csv"

    if os.path.exists(feather_file):
        print(f"Loading game data for {set_code} from Feather file...")
        try:
            df = pd.read_feather(feather_file)
            games_dfmap[set_code] = df
            return df
        except Exception as e:
            print(f"Error loading Feather file {feather_file}: {e}. Attempting to re-convert from CSV.")
            # If Feather fails, try to re-convert from CSV
            if os.path.exists(csv_file):
                df = convert_to_feather_(set_code)
                games_dfmap[set_code] = df
                return df
            else:
                raise FileNotFoundError(f"Neither Feather nor CSV file found for set: {set_code}") from e


    if os.path.exists(csv_file):
        print(f"Reading and converting data for {set_code} to Feather...")
        df = convert_to_feather_(set_code)
        games_dfmap[set_code] = df
        return df

    raise FileNotFoundError(f"No data found (Feather or CSV) for set: {set_code}")

def convert_to_feather_(set_code: str):
    """
    Converts the games CSV file to Feather format for efficient storage and retrieval.
    This function will overwrite an existing Feather file if a CSV exists.

    Args:
        set_code (str): The code for the game set.

    Returns:
        pd.DataFrame: The newly converted DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    csv_file = f"data/{set_code}/games.csv"
    feather_file = f"data/{set_code}/games.feather"

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file {csv_file} does not exist.")

    print(f"Converting {csv_file} to {feather_file}..., low mem")
    print(f"Memory usage before reading CSV: {psutil.virtual_memory().used / (1024 * 1024):.1f} MB")
    #df = pv.read_csv(csv_file)
    print(f"Memory usage after reading CSV: {psutil.virtual_memory().used / (1024 * 1024):.1f} MB")
    df = pd.read_csv(csv_file, low_memory=True)
    # Using 'zstd' for good compression and performance, 'lz4' is an even faster option
    print("No compression")
    df.to_feather(feather_file, compression="none")
    print(f"Successfully converted {csv_file} to {feather_file}.")

    # Update cache if conversion was successful
    games_dfmap[set_code] = df
    return df

blb_df = get_games_data('blb')

blb_df.head()