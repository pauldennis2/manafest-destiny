### Good factors/potential unexplored areas:

1. With clustering, we can do something similar to what we did with synergy - determine which cards stand out specifically in each archetype, and add that as a feature to our model. We could also look at factors like archetype specific curves, creature counts, and so on. 
2. We have so far been only using a fraction of our data, but we *should* be ready (after some code cleanup) to scale up. Feeding in 10x as much data should help our deep NN model learn better. 
3. The models train extremely fast. Even our random hyperparameter search lasted only five minutes. This means we have a lot of room to explore deeper models, grid searches, and so on. 

### Difficulty factors 

1. Lots of code cleanup needed 
2. Even after substantial feature engineering and model tuning, we are really struggling to predict win rates. This problem may just be less amenable to this type of modeling than we had hoped. 


### Areas to explore 
1. We considered trying to apply a "deconfounding luck" factor. Looking at things like, how many times did this deck "have to" take a mulligan, how often did it draw its bombs. We could then apply a slight adjustment to the win rate and ask our model to predict that "luck adjusted win rate". So a deck that went 7-1 (87.5% win rate) that drew its main bomb every single game and never had to take a mulligan might be adjusted down to an 80% expected win rate, and conversely a deck with poor luck factor would be moved up. 
2. We might want to explore rank as a factor. There are substantial differences in win rates across ranks, so this also might play into an adjusted win rate factor. 
3. We may need to explore time as a factor.
4. Feature scaling/tuning may be a big potential win.