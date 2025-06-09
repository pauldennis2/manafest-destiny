# MTG Primer

In this document, we'll provide an introduction for people who are unfamiliar with the game. We recommend everyone read the first section; further sections are NOT essential reading but will help explain some jargon and provide deeper understanding.

## Basic Core Concepts Required to Understand Project (Read this!)

For readers unfamiliar with Magic: The Gathering (MTG), this brief primer provides essential context to understand the project's data and objectives. We won't teach you how to play, but we'll cover the fundamental terms relevant to our analysis.

* **Card:** The basic unit of MTG. Cards represent spells, creatures, or other game elements. Each card has a **mana cost** (how much mana is needed to play it), a **type** (e.g., Creature, Sorcery, Land), and a text box describing its abilities. Creatures also have **Power** (how much damage they deal) and **Toughness** (how much damage they can take).
* **Deck:** The cards a player uses to play the game. The "decklist" is the primary input our model uses to predict performance.
* **Set:** A distinct collection of around 150-200 unique cards released together. Sets often have their own themes and mechanics. When we refer to a "Bloomburrow draft," we mean a game played using only cards from the Bloomburrow set. Because each set has a unique card pool, models trained on one set generally can't predict performance in another.
* **Limited Play** A popular MTG format where players don't bring their own pre-built decks.  Players build a 40-card deck from packs of random cards. This format emphasizes strategic card evaluation and on-the-fly deck construction. [**Draft**](https://magic.wizards.com/en/formats/booster-draft) is the format we are focused on. 

* **Mana:** The fundamental resource used to cast spells and activate abilities in MTG. Players typically generate mana using **Land** cards. Each card requires a specific amount of mana to be played. Converted Mana Cost (CMC) represents this numerically.

For a deeper dive into MTG fundamentals, you can check out the official [Magic: The Gathering](https://magic.wizards.com/en/news/feature/level-one-full-course-2015-10-05) intro.

## Drafting Process and Strategies

### Process

You can think of an MTG draft as similar to a draft for a sports team, but instead of the pickers taking turns from the same pool, picking occurs simultaneously from individual packs of cards.

1. Eight players sit down at a table (virtual table if online).
2. Each player starts with three booster packs in front of them.
3. In the first round, each player opens one pack, chooses ONE card out of that pack, and passes the remainder to the player on their left.
4. You then choose one card from the cards that were passed to you; this process continues until all 15 cards are picked.
5. In the second round, players open their second pack, and the same process is followed, but passing cards to the right.
6. In the final round, players open the final pack and return to passing left.
7. At the end of the process each player has 45 cards; they use ~23 of these cards, and basic lands (provided separately) to create a deck with 40 cards.

Based on these numbers, it's clear that not every pick has to be a card you plan to include, but most of your early picks should wind up in your deck.

### Strategy

**Forcing an Archetype**: Generally not the best strategy, but it is simple. The player decides very early on (either before opening the first pack or within the first 1-2 choices) to "force" a certain strategy. "I'm going to draft Green/White rabbits no matter what." The advantage of this approach is it keeps your draft consistent - you always know what you're looking for and avoid the problem of lurching between different tribes. The downside is it is very inflexible and doesn't adapt to the circumstances on the ground. It's kind of like saying in football, "we're going to keep running the ball on every play, even if it isn't working."

**Finding Your Lane**: In modern drafts there are generally 10 possible lanes/archetypes, and 8 players at a table. Drafters are actually incentivized to cooperate, but are not allowed to communicate other than through card picks. Finding a lane that no one else is in is generally the best strategy. If two or more players are fighting over a lane, they both end up worse off.

**Signalling**: Heavily related to determining lane. We can split this into "reading signals" and "sending signals". 

**Reading**: A lot of this comes down to likelihood, not certainties. If you're looking at a pack 5 people have already picked from and seeing two really strong Frog cards, it's likely that none of those players are in the "Frog lane". This increases the chance you will get passed more good Frog cards later in the draft.

**Sending**: Let's say you open your first pack and see three really strong Black cards and one really good Green card. Your natural instinct might be to say "Black is abundant, I'm grabbing one of these". The problem is that you are passing two great black cards. This increases the chance that downstream players will draft Black, reducing the likelihood of strong Black cards coming back to you in future rounds. If you take the only green card in the pack, this creates a signal - "Green is taken" - which pushes other players to the other colors, and makes it more likely you'll see good green cards later.

## High Level Deck Strategies

These are high-level generalizations and because of the randomness of drafting, there are always exceptions.

**Early Aggression**: This strategy focuses on overwhelming the opponent early with low-cost aggressive creatures. Before they can even set up their strategy, we've won the game. If it fails to establish an advantage early, this deck will almost always lose. Typical colors: White, Red.

**Midrange**: Survive the early game and put out larger threats that can efficiently deal with early aggression. We're focused on the midgame. Typical colors: Green.

**Control**: Focuses more on reacting to the opponent's strategy, using removal and counter magic. Plays defensively early on, and usually tries to close out with a large threat when the opponent is out of gas. Typical colors: Blue, Black.

**Grind**: Focuses on long-term efficiency, often using lifegain strategies to outlast the opponent. Tends to be equally strong at all phases, focused on "stalling" the game. Typical colors: White, Black.