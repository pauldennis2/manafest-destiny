## Root

### Data

 * Each set's data is stored in its own folder, named with the 3-letter set code. (Bloomburrow = blb)
 * Game (deck) data (very very big) is saved as games.csv, and then converted to games.parquet
    - Added via manual download as games.csv, very big (2.6G)
    - Converted to games.parquet (59M)
 * Card data (small)
    - Fetched from Scryfall API and saved as cards_full.csv
    - Cleaned of unneeded columns and saved as cards.csv
 * Both processes will check first for data in memory, then in the file system then (in the case of card data) on the API

 ### Scripts

  * `deckcard_analysis.py`: does the thing
  * `get_card_data.py`: other thing
  * `modeling.py`: third thing
  * `get_deck_data.py`: Convert data to Parquet, 
