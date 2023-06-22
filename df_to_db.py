import pandas as pd
import sqlite3

# Read the CSV file
df = pd.read_csv('data.csv')

# Connect to the SQLite3 database
conn = sqlite3.connect('vedas.db')

# Write the DataFrame to an SQLite3 table
df.to_sql('threat', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
