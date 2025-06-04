import pandas as pd
df = pd.DataFrame({'a': range(1000), 'b': range(1000)})
df.to_feather('test_small.feather')

# Try reading it back
df2 = pd.read_feather('test_small.feather')
print("Small file worked")