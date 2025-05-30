"""
 __ _                               _     _ _        
/ _\ |_ __ _ _   _    __ ___      _| |__ (_) | ___   
\ \| __/ _` | | | |  / _` \ \ /\ / / '_ \| | |/ _ \  
_\ \ || (_| | |_| | | (_| |\ V  V /| | | | | |  __/_ 
\__/\__\__,_|\__, |  \__,_| \_/\_/ |_| |_|_|_|\___( )
             |___/                                |/ 
                  _   _ _     _                      
   __ _ _ __   __| | | (_)___| |_ ___ _ __           
  / _` | '_ \ / _` | | | / __| __/ _ \ '_ \          
 | (_| | | | | (_| | | | \__ \ ||  __/ | | |         
  \__,_|_| |_|\__,_| |_|_|___/\__\___|_| |_|         
                                                   
"""

def analyze_deck_two(): #TODO defos change
    # Create empty Deck DataFrame with dynamic type columns
    deck_columns = ["deck_id", "wins", "losses", "avg_mana_curve", "bomb_density", "color_identity"] + [f"num_{ctype.lower()}" for ctype in card_types]
    deck_df = pd.DataFrame(columns=deck_columns)

    # Aggregate deck data
    grouped = draft_df.groupby("deck_id")

    for deck_id, group in grouped:
        deck_list = group["card_name"].tolist()

        # Compute core metrics
        wins = group["wins"].sum()
        losses = group["losses"].sum()
        
        # Filter out lands before calculating mana curve
        non_land_cards = [card for card in deck_list if "Land" not in card_df.loc[card, "type_line"]]
        avg_mana_curve = sum(card_df.loc[card, "cmc"] for card in non_land_cards if card in card_df.index) / len(non_land_cards) if non_land_cards else 0

        bomb_density = sum(1 for card in deck_list if card_df.loc[card, "rarity"] in ["rare", "mythic"]) / len(deck_list)
        color_identity = list(set(color for card in deck_list for color in card_df.loc[card, "color_identity"]))

        # Count card types dynamically
        type_counts = {f"num_{ctype.lower()}": sum(1 for card in deck_list if ctype in card_df.loc[card, "type_line"]) for ctype in card_types}

        # Append to deck_df
        deck_df.loc[len(deck_df)] = {
            **{"deck_id": deck_id, "wins": wins, "losses": losses, "avg_mana_curve": avg_mana_curve, "bomb_density": bomb_density, "color_identity": color_identity},
            **type_counts
        }

    # Save the structured deck data
    deck_df.to_csv("deck_analysis.csv", index=False)

    print(f"Deck DataFrame created: {deck_df.shape[0]} rows, {deck_df.shape[1]} columns")
    return deck_df

def analyze_first_full_draft(games_df):
    """
    Takes a Pandas DataFrame (`games_df`), finds the first complete draft, 
    calculates its win rate, and returns the raw decklist.

    Returns:
        dict: Raw decklist with card names as keys and counts as values.
    """

    if games_df.empty:
        print("Error: DataFrame is empty. Cannot analyze draft.")
        return {}

    # Identify the first draft_id
    first_draft_id = games_df["draft_id"].iloc[0]
    print(f"\nAnalyzing data for draft_id: {first_draft_id}")

    # Filter for all rows belonging to this draft_id
    first_draft_df = games_df[games_df["draft_id"] == first_draft_id].copy()

    # --- Calculate Win Rate ---
    total_wins = first_draft_df["won"].sum()
    total_games = len(first_draft_df)
    total_losses = total_games - total_wins

    win_rate = (total_wins / total_games) * 100 if total_games > 0 else 0.0

    print(f"\n--- Draft Performance for {first_draft_id} ---")
    print(f"Event Record: {total_wins}-{total_losses}")
    print(f"Win Rate: {win_rate:.2f}%")

    # --- Extract Decklist ---
    deck_card_columns = [col for col in first_draft_df.columns if col.startswith("deck_")]
    deck_composition_row = first_draft_df[deck_card_columns].iloc[0]

    # Convert to dictionary format: {card_name: count}
    decklist_raw = {
        col.replace("deck_", ""): int(deck_composition_row[col])
        for col in deck_composition_row.index
        if deck_composition_row[col] > 0
    }

    return decklist_raw  # Now returning the decklist for further enrichment

def enhanced_deck_analysis():
    # Convert decklist dictionary to DataFrame
    decklist_df = pd.DataFrame(decklist_raw.items(), columns=["name", "count"])

    # Merge with Scryfall card data
    decklist_enriched = decklist_df.merge(cards_df[["name", "cmc", "type_line"]], on="name", how="left")

    # Compute basic deck stats
    avg_mana_value = (decklist_enriched["cmc"] * decklist_enriched["count"]).sum() / decklist_enriched["count"].sum()
    num_creatures = decklist_enriched[decklist_enriched["type_line"].str.contains("Creature", na=False)]["count"].sum()

    # Display enriched decklist with stats
    print(f"\n--- Enhanced Deck Analysis ---")
    print(f"Average Mana Value: {avg_mana_value:.2f}")
    print(f"Total Creatures: {num_creatures}")
    print(decklist_enriched[["name", "count", "cmc", "type_line"]])

# Step 4: Extract Card Types
def get_card_types(card_df: pd.DataFrame) -> set:
    """Finds all distinct card types in the dataset."""
    return {type_line.split()[0] for type_line in card_df["type_line"]}

# Step 5: Compute Deck Data
def generate_deck_data(draft_df: pd.DataFrame, card_df: pd.DataFrame, output_file: str, max_decks: int = None) -> None:
    """Aggregates deck performance data with an optional limit and saves it to a CSV file."""
    card_types = get_card_types(card_df)
    #deck_columns = ["deck_id", "wins", "losses", "avg_mana_curve", "bomb_density", "color_identity"] + [f"num_{ctype.lower()}" for ctype in card_types]
    
    # Draft id from that DF just becomes "deck_id" in the final
    grouped = draft_df.groupby("draft_id")
    deck_columns = [col for col in draft_df.columns if col.startswith("deck_")]
    deck_df = pd.DataFrame(columns=deck_columns)

    for i, (deck_id, group) in enumerate(grouped):
        if max_decks and i >= max_decks:
            break  # Stop early if max_decks is reached
        
        # Get list of card names from relevant columns
        deck_list = [col.replace("deck_", "") for col in deck_columns if group[col].sum() > 0]

        wins, losses = group["wins"].sum(), group["losses"].sum()

        non_land_cards = [card for card in deck_list if "Land" not in card_df.loc[card, "type_line"]]
        avg_mana_curve = sum(card_df.loc[card, "cmc"] for card in non_land_cards if card in card_df.index) / len(non_land_cards) if non_land_cards else 0
        bomb_density = sum(1 for card in deck_list if card_df.loc[card, "rarity"] in ["rare", "mythic"]) / len(deck_list)
        color_identity = list(set(color for card in deck_list for color in card_df.loc[card, "color_identity"]))
        type_counts = {f"num_{ctype.lower()}": sum(1 for card in deck_list if ctype in card_df.loc[card, "type_line"]) for ctype in card_types}

        deck_df.loc[len(deck_df)] = {**{"deck_id": deck_id, "wins": wins, "losses": losses, "avg_mana_curve": avg_mana_curve, "bomb_density": bomb_density, "color_identity": color_identity}, **type_counts}
    deck_df.to_csv(output_file, index=False)
    print(f"Deck DataFrame created: {deck_df.shape[0]} rows, {deck_df.shape[1]} columns (Processed up to {max_decks} decks)")

