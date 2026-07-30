import pandas as pd

# CORRECTED PATH - Your file is at D:\prg200
df = pd.read_csv(r'D:\prg200\nepal_bank_transactions.csv')

# Display the first five and last five rows of the DataFrame
first_five_rows = df.head()
last_five_rows = df.tail()

print(f"Features :\n{df.columns}")

print("First five rows of the DataFrame:")
print(first_five_rows)
print("\nLast five rows of the DataFrame:")
print(last_five_rows)

print(f"Row count: {df.shape[0]}, Column count: {df.shape[1]}")

print(f"DataFrame Info:")
print(df.info())

print(f"DataFrame Description:")
print(df.describe())

# select single column
print(f"channel:\n{df['channel'].head()}")

# select multiple columns
print(f"channel and amount:\n{df[['channel', 'amount_npr']].head()}")