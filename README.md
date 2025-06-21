# Manafest Destiny

Welcome to Manafest Destiny, a data science project to develop a regression model for analyzing Magic: The Gathering (MTG) draft decks. This file will serve as a directory to other areas.

First, if you are not familiar with Magic, I highly recommend you read at least the first two sections of the [MTG Primer](mtg_primer.md). This should provide enough understanding to get the gist of the project.

The final/core analysis for "Version 1" is contained in the [Presentation Notebook](presentation_notebook.ipynb). This is effectively a pruned version of the analysis process that includes EDA and the final features and models used, as well as showing some steps. The [Bloomburrow Modeling](blb_modeling.ipynb) notebook contains more of the messy details of the process including a lot of exploration of neural networks as well as other attempts that didn't pan out.

There are other files that contain supplemental information, but those are the core.

The three data sources used for the project:

* **[17Lands Game Data](https://www.17lands.com/public_datasets)**: This platform provides detailed draft and game data from *Magic: The Gathering Arena*. Each row in our dataset represents a single game, including the full decklist used and the match results. This offers the empirical performance data crucial for our predictions.
* **[Scryfall Card Data](https://scryfall.com/)**: As a comprehensive database for Magic: The Gathering cards, Scryfall allows us to enrich our raw 17lands data. Basic 17lands data often only provides card names. We use Scryfall to retrieve detailed attributes for each card. This enrichment step is important for creating meaningful features for our model.
* **[17Lands Card Ratings](https://www.17lands.com/card_data?expansion=BLB&format=PremierDraft)**: The 17Lands card data, providing win rate information on individual cards, is also an important source of enrichment for the analysis.

P.S.: The name "17Lands" comes from the typical number of basic lands that players include in draft decks of 40 total cards.
