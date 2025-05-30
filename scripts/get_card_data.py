"""
Responsible for getting the card data from the API and saving it to a file.

Cleaning included free of charge.
"""

import requests
import os
import pandas as pd

card_dfmap = {} # Map to orgnaize card data by set code

SET_CODES = {'blb': 'Bloomburrow', 'dsk': 'Duskmourn'} # Simply for pretty printing; not required
def get_card_data(set_code: str) -> pd.DataFrame:
    """Fetches Scryfall data for a specific set and saves it to a CSV file.
    If the CSV already exists, it loads the data from there instead of fetching it again.

    This data is paginated, so it will fetch all pages until no more data is available.

    Set codes: https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_sets

    e.g Bloomburrow = "blb"
    """
    set_name = set_code # If available, use the set name for pretty printing
    if set_code in SET_CODES:
        set_name = SET_CODES[set_code]
    # 1. Check if the card data is already in the map
    if set_code in card_dfmap:
        print(f"Retrieved {set_name} data from memory.")
        return card_dfmap[set_code]

    # 2. If not, check if the CSV file exists
    file_path = f"data/{set_code}/cards.csv"
    if os.path.exists(file_path):
        print(f"Loading Scryfall data for {set_name} from existing file...")
        df = pd.read_csv(file_path)
        card_dfmap[set_code] = df
        return df
    
    # 3. If neither, fetch the data from Scryfall API
    print(f"Fetching Scryfall API data for {set_name}...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
    url = f"https://api.scryfall.com/cards/search?q=set:{set_code}"
    all_data = []  

    while url:
        response = requests.get(url)
        response_data = response.json()
        
        all_data.extend(response_data["data"])
        
        # Check if there are more pages
        url = response_data.get("next_page", None)  # Fetch next page if available

    # Convert full dataset to DataFrame and save
    df = pd.DataFrame(all_data)
    df.set_index("name", inplace=True)
    df.to_csv(file_path, index=False)
    card_dfmap[set_code] = df
    return df

# Not sure what I want  to do with this yet
def clean_card_data_(card_df: pd.DataFrame, output_file: str) -> None:
    """Cleans the card dataset by dropping unnecessary columns and saving the processed version."""
    core_card_data = ["name", "mana_cost", "cmc", "type_line", "oracle_text", "colors", "color_identity", "keywords", "rarity", "power", "toughness"]
    skeptical_keepers = ["reprint"]
    external_references = ["oracle_id", "multiverse_ids", "mtgo_id", "arena_id", "tcgplayer_id", "cardmarket_id"]
    status_and_printing = ["foil", "nonfoil", "promo", "reprint", "variation", "security_stamp", "frame", "full_art", "textless"]
    art_and_flavor = ["artist", "illustration_id", "flavor_text", "border_color"]
    marketplace_and_pricing = ["prices", "purchase_uris", "related_uris"]
    metadata_and_links = ["set", "set_name", "set_type", "set_uri", "set_search_uri", "scryfall_set_uri", "rulings_uri", "prints_search_uri", "collector_number"]

    drop_list = external_references + status_and_printing + art_and_flavor + marketplace_and_pricing + metadata_and_links
    
    card_df.drop(columns=drop_list, inplace=True)
    card_df.to_csv(output_file, index=False)
    print(f"Processed data: {card_df.shape[0]} rows, {card_df.shape[1]} columns")
    print(f"Cleaned file saved as {output_file}")