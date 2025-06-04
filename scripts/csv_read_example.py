# Let first 16 columns infer naturally, force rest to int8
dtype_dict = {i: 'int8' for i in range(16, 1398)}
# Columns 0-15 will use pandas' default inference

df = pd.read_csv('your_file.csv', dtype=dtype_dict)