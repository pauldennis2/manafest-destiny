# Mana-fest Destiny

(Summary created by Gemini, edited by author)

## Project Overview
Mana-fest Destiny is a data science project focused on **predicting deck performance in Magic: The Gathering (MTG) draft formats**. Using regression modeling and advanced statistical analysis, the goal is to develop a scalable, idempotent framework for evaluating the viability of draft decks based on various in-game parameters.

## Objectives
- **Develop a regression model** to predict deck performance based on draft choices.
- **Analyze cross-set learning** to determine how well models generalize across different MTG expansions.
- **Ensure idempotency** in data processing workflows for consistent, repeatable analysis.
- **Optimize scalability** to accommodate large datasets and evolving deck strategies.
- **Refine draft evaluation metrics** using domain knowledge and empirical testing.

## Approach
- Collect and preprocess draft data from available sources.
- Engineer relevant features to enhance model performance.
- Experiment with multiple regression techniques and validation strategies.
- Implement sustainable **Docker workflows** for machine learning frameworks.
- Iterate model refinements based on performance benchmarks.

## Dependencies
- **Python** (with an emphasis on modular, scalable design)
- **Pandas / NumPy** for data manipulation
- **Scikit-learn** for machine learning modeling
- **Docker** for environment management
- **MTG dataset sources** (to be specified)

## Future Considerations
- Expanding the project to **incorporate alternative machine learning techniques** such as deep learning.
- Investigating meta-strategies that **optimize draft choices dynamically**.
- Structuring the workflow for potential **collaborative contributions**.


# Captain's Log, Stardate 0246.3

Gemini continues to summarize our further design steps and discussions below (edited).

# Detailed Project Approach & Domain Insights


This section delves into the specific methodologies and domain-centric considerations guiding the Mana-fest Destiny project.

### Data Acquisition & Enrichment
Our analysis relies on two primary data sources:
* **[17lands.com](https://www.17lands.com/)**: This platform provides detailed draft and game data from *Magic: The Gathering Arena*. Each row in our dataset represents a single game, including the full decklist used and the match results. This offers the empirical performance data crucial for our predictions.
* **[Scryfall.com](https://scryfall.com/)**: As a comprehensive database for Magic: The Gathering cards, Scryfall allows us to enrich our raw 17lands data. Basic 17lands data often only provides card names. We use Scryfall to retrieve detailed attributes for each card. This enrichment step is vital for creating meaningful features for our model.

### Defining Deck Performance
In MTG Arena's draft format, a player continues playing until they achieve **7 wins or 3 losses**, whichever comes first. This creates an **asymmetrical win/loss record system** (e.g., 7-0, 7-1, 7-2 are all wins, while 6-3, 5-3, 4-3, 3-3, 2-3, 1-3, 0-3 represent progressively worse outcomes). Our goal is to predict this "performance" record for a given decklist. A critical data consideration involves handling "unfinished rounds," where players might abandon a draft midway (e.g., at a 5-2 record). We will analyze the prevalence of such records and determine the most appropriate strategy for their inclusion or exclusion in our dataset.

### Core Modeling & Feature Engineering
We aim to develop a regression model that, given a decklist, predicts its average performance. **XGBoost** is a strong candidate. 

A significant focus of this project will be **custom feature engineering**, leveraging deep domain knowledge of Magic: The Gathering. One key example is the **"mana curve perturbation score"**:

* **Mana Curve Context**: In Magic: The Gathering, a deck's "mana curve" refers to the distribution of its cards' converted mana costs (CMC). A well-balanced mana curve ensures a player can consistently cast spells throughout the game, matching the tempo of the format. Different sets or strategies might favor different mana curve shapes.
* **Perturbation Score**: This feature quantifies how much a specific deck's mana curve deviates from an optimal or recommended distribution for its particular draft format. This could be defined against static recommendations or dynamically derived from the mana curves of high-performing decks within the relevant dataset.

### Cross-Set Generalization Challenge - Stretch Goal
A fascinating aspect of this project is the challenge of **cross-set learning**. Models trained on data from one MTG set (e.g., Bloomburrow) are unlikely to generalize well to predict performance in drafts from a different set (e.g., Duskmourne). This is primarily because many high-impact features are card-specific ("Does this deck contain Card X?"), and the card pools change entirely between sets. Our analysis will explore the extent of this generalization gap and consider approaches for creating more robust, transferrable features that capture abstract strategic elements rather than specific card identities.

### Visual Storytelling - Stretch Goal/Prework
Beyond the core data science, we are incorporating custom visual elements to enhance the project's presentation. This includes a unique project logo and ten heraldry-style icons representing the different tribes within the Bloomburrow set. These visuals are intended to help tell a more engaging story and make the project stand out, reinforcing the blend of analytical rigor and domain passion.

# Stardate 304.6

Gemini describes the MVP and some very basic MTG concepts (substantially edited).

## Minimum Viable Product (MVP) & Project Scope

Our **Minimum Viable Product (MVP)** for Mana-fest Destiny is to successfully predict the performance of decks drafted specifically in the **Bloomburrow** set. This focused approach allows us to establish a robust prediction model and workflow within a single, consistent environment.

While our **Future Considerations** (e.g., Cross-Set Generalization) outline ambitious long-term goals, we are explicitly identifying them as **stretch goals** beyond the initial MVP. This ensures we deliver a complete and impactful core project first.

---

## MTG Primer for the Uninitiated

For readers unfamiliar with Magic: The Gathering (MTG), this brief primer provides essential context to understand the project's data and objectives. We won't teach you how to play, but we'll cover the fundamental terms relevant to our analysis.

* **Card:** The basic unit of MTG. Cards represent spells, creatures, or other game elements. Each card has a **mana cost** (how much mana is needed to play it), a **type** (e.g., Creature, Sorcery, Land), and a text box describing its abilities. Creatures also have **Power** (how much damage they deal) and **Toughness** (how much damage they can take).
* **Deck:** The cards a player uses to play the game. The "decklist" is the primary input our model uses to predict performance.
* **Set:** A distinct collection of around 150-200 unique cards released together. Sets often have their own themes and mechanics. When we refer to a "Bloomburrow draft," we mean a game played using only cards from the Bloomburrow set. Because each set has a unique card pool, models trained on one set generally can't predict performance in another.
* **Limited Play** A popular MTG format where players don't bring their own pre-built decks.  Players build a 40-card deck from packs of random cards. This format emphasizes strategic card evaluation and on-the-fly deck construction. [**Draft**](https://magic.wizards.com/en/formats/booster-draft) is the format we are focused on. 

* **Mana:** The fundamental resource used to cast spells and activate abilities in MTG. Players typically generate mana using **Land** cards. Each card requires a specific amount of mana to be played. Converted Mana Cost (CMC) represents this numerically.

For a deeper dive into MTG fundamentals, you can check out the official [Magic: The Gathering](https://magic.wizards.com/en/news/feature/level-one-full-course-2015-10-05) intro.