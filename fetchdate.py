import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('vedas.db')
cursor = conn.cursor()

# Fetch the dates from the threat table
cursor.execute("SELECT TIMESTAMP FROM threat")
rows = cursor.fetchall()

# Extract the unique dates from the timestamps
dates = set()
for row in rows:
    timestamp = row[0]
    # Parse the timestamp
    dt = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S:%z")
    # Extract the date
    date = dt.date()
    dates.add(date)

# Print the unique dates
for date in dates:
    print(date)

# Close the connection
conn.close()
