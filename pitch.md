# Manafest Destiny Pitch

## Business Problem Scenario

### Business Problem Statement

Gathering Analytics, Inc has approached our firm for this project. They are seeking to break into the Magic the Gathering online market by launching a website that will offer detailed guidance backed by data, as well as developing AI coaching services. They want to start with a model that can analyze the performance of draft decks. This analysis will inform recommendations for drafting strategies.

The team at GA inc, our stakeholders, includes a few people who are very familiar with the game and its mechanics, but also marketing and executive professionals. We will need to clearly communicate the essential game concepts when presenting our findings.

### Primary Goals

### Machine Learning

Machine learning is a perfect fit for this problem. First, we have ample high-quality structured data to work with, courtesy of [17Lands](www.17lands.com). Second, this is a complex problem space with a large number of interacting features. In order to create a modeling process that is extensible to future sets, we need to be able to learn general patterns in the data.

### Data

#### Core

The core data set is from [17Lands](https://www.17lands.com/public_datasets). We have selected the Bloomburrow set, a popular recent release. There are three types of data available here:

- **Draft Data**: Captures the actual choices players made during the drafting portion (which cards they chose, which they passed). This is an extremely detailed and rich source of information that would be an excellent opportunity for future analysis. Each row represents one pick for a given player's draft.

- **Game Data**: Captures high level information about the games: what cards the player had in their deck and drew, general archetype information about their deck, and the win/loss result. This is our **core analysis target**. Each row represents one game.

- **Replay Data**: Captures extremely detailed information about each game, showing exactly what happened on each turn. Another very detailed and potentially rich source of information for analyzing play patterns. Each row represents one turn in a game.

If we were to think about this in football terms, the Draft Data is a like a record of the NFL draft, where players are chosen for different teams. The Game Data is high level information about each game - the final score, total yards by each team, and so on. The Replay Data is like a video of the entire game.

#### Game Data Details

This is our core analysis target. We have chosen one particular set called "Bloomburrow" which focuses on tribes of small critters (otters, rabbits, lizards, and so on). We chose the "Premier Draft" as this is the most common format for high-level play. Players complete a full draft to build their deck (check [here](https://github.com/pauldennis2/manafest-destiny/blob/main/mtg_primer.md) for a full description). They then play until they reach 7 wins or 3 losses (or decide to stop). This asymetrical factor is something we have to account for, but will not pose a substantial problem as there is a clear ordering for completed drafts.

The dataset is truly massive, weighing in around 2.6 gigabytes in raw CSV form. There are almost a million games (rows), with each row having over 1300 columns. There are ~260 cards in the set, and each card is represented in five columns (representing whether it was in the deck, drawn in the game, present in the opening hand, or available in the "sideboard"). Our main focus is on using the "deck" columns to create the decklist, which will be our core predictive input.

One very important note about our data: 17Lands relies on players choosing to "log" their drafts and upload their data, so our data has an inherent **selection bias**. The average win rate is around 54%. This is because players who are interested enough to go to the trouble of recording their process are more invested in the game, and spend more time researching and trying to learn from top players.

This is not really a problem for our stakeholder though, as it is *exactly* this type of player that they are looking to attract to their website. The more casual players who do a draft occasionally for fun are not looking for paid AI draft coaching services.

#### Supplemental

We have brought in two supplemental data sources that provide more detailed information about the cards in the set. We could think about these like detailed scouting reports for every player on an NFL team.

- **Scryfall Card Data**: This gives us information about the types and mechanics of cards - mana cost, keyword abilities, and so on. Available through API access [here](https://api.scryfall.com/cards/search?q=set:blb). This is similar to information about a player like height, weight, age, and so on.

- **17Lands Card Stats**: This gives us information about the actual performance of the cards - different ways of measuring how they impact the outcome. This would be similar to player information such as total yards, number of interceptions, and so on.

Together, these two sources provide essential context that we will use to enhance our analysis of game data. Both supplemental sets contain one row per card (~260) with about 45 fields for Scryfall and 12 for 17Lands cards. The Scryfall data contains a large amount of information that is irrelevant for our analysis.

#### Relevance

Since our goal is developing a data-based understanding of MTG drafts, this data couldn't be more relevant to our problem. The 17Lands "Game" data is the direct representation of our core target: deck lists with win/loss information. The supplemental sets provide context.

### Measuring Success

The outcome we are trying to predict is highly variable. Win rate is determined from as few as 3 games or as many as 9, and each individual game's outcome is highly dependent on random luck (card draws), as well as a "matchup luck" factor - sometimes a player will be matched against an opponent of greater skill or using a deck that naturally counters theirs. Think of it like poker - in any given hand (game), the best poker player in the world could lose to someone with only a moderate understanding of the game. Our data is similar - good players distinguish themselves over many different games and drafts.

The goal is not to bet on win rate outcomes, so the actual prediction itself is **not** the most important factor. We want to use this predictive process to gain insights that our client can use as inputs to their coaching process. For example, if we determine that sticking closely to 1 or 2 colors is highly correlated with win rates, this conclusion feeds into better understanding how to draft: choose colors early and stick with them. On the other hand, if we find that high-value individual cards are the most important factor, we would recommend the opposite: don't be afraid to change your plan to pick up a high impact card.

Given the high variability from luck, we can expect our model to struggle to explain more than 15% of the variability (i.e. R-squared value of 0.15). Win rates vary all the way from 0 to 1, and even top players are not able to reliably predict how a given draft deck will do.

Our main measure of success will be in extracting **interpretable and communicable** insights about which factors are the biggest drivers of performance. An arcane formula like "If you take the cube root of the number of Forests in your deck and raise it to the power of your most expensive card, divide it by the natural log of the number of creatures, this number predicts success." Even if this *were* a predictor of win-rate, it gives a player no usable advice that can shape their draft.

## Problem Solving Process

### Data Acquisition and Understanding

The data is graciously provided by 17Lands, downloadable as a compressed CSV. We have already secured the data for our target set and completed a basic analysis. There are a very small number of records with "impossible" results that we have dropped, but these represent a tiny edge case (0.01%). The Scryfall data is easiest to access through an API call for our current purposes. Because this data is collected in a very automated way, it avoids pitfalls of randomly missing entries or data entry errors. 

We will perform EDA primarily on the game data and the Scryfall card data, with the focus on the target (game data). We will explore the distribution of win-loss records (how many 7-2s, 6-3s, 1-3s, 0-3s, and so on), as well as the prevalence of different archetypes. Determining how many of the drafts are incomplete is an early priority.

### Data Preparation and Feature Engineering

Again, because the data does not rely on manual entry, there is minimal cleaning required. The Scryfall data contains some non-draft cards, which we will remove. We drop the "impossible" records discussed previously (like a 7-3 or 5-4 record). We will decide how to handle incomplete records based on their prevalence.

Feature engineering is a core aspect of this project. Simply feeding the deck lists into a machine learning algorithm would be inefficient and likely cause overfitting to specific patterns of cards that aren't truly predictive. We will explore several "score" features such as:

 - Mana curve (how "fast" or "slow" the deck is)
 - Synergy (how well the cards in the deck work together)
 - Bombs (how many powerful game-winning cards the deck contains)
 - Removal (how prepared the deck is to deal with the opponent's game plan)

These features are based on well-understood *intuitive* principles of drafts, but the value of our model is that we will be able to quantify these factors on a **set-by-set basis**. While there are overarching themes and general rules of thumb, each new set brings its own challenges; early and accurate analysis of a new draft set is a valuable commodity for competitive players, just as detailed scouting on players is valuable to a sports team.

### Modeling Strategy

Given that this is a high-dimensional problem with complex interactions, we feel that neural networks (Multilayer perceptrons) will likely offer the most predictive power. We will use linear regression as a "naive baseline" to test our engineered features, but we expect this to be of limited use. Random forest and XGBoost will be the primary pacers for the neural model.

Hyperparameter tuning will depend on the model chosen; if NN, using Keras/Tensorflow tuners is the default. We'll employ cross-validation and train/test/validate splits to ensure model performance holds up on unseen data.

For evaluation metrics, R-squared and Mean Absolute Error (MAE) are the core metrics. As noted previously, these values need to be interpreted in context; this is a highly random space, so predictive power is inherently limited. We'll explore ways to correct for the random nature to bring out the deterministic factors that matter most.

### Results Interpretation and Communication

First, we believe the biggest challenge may be to appropriately communicate the necessary information about the game itself to people who have never played it. We've started with a "MTG Primer" for the uninitiated, targeted specifically at explaining just enough to get the essential factors for this project. We'll also provide links to other resources and some "deeper dives" for those who are interested. All core results will be communicated in a manner accessible to a general audience who have read our basic primer.

The primary conclusions we draw from the model will **not** be highly technical in a statistical sense.

## Timeline

 1. Dataset finalization and problem formulation - **4 hours**. The data is easy to access, and we'll invest some time in examining compression methods.
 2. Exploratory Data Analysis - **10 hours**. Given the substantial size of the core data set as well as supplemental data, basic EDA will be a substantial time commitment.
 3. Data Preprocessing - **20 hours**. We've already established cleaning will be minimal and feature engineering will consume the most time.
 4. Model Development - **12 hours**. We have three well-defined model approaches. We'll need to experiment to see how feature engineering works and whether full card information is a help or hindrance.
 5. Model Evaluation and Refinement - **6 hours**.
 6. Documentation and Reporting - **10 hours**. We'll need to allow substantial time to clean up our lengthy process and think about how best to communicate our findings to non-MTG experts.
 7. Final Review and Submission - **4 hours**. 