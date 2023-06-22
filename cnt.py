import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('vedas.db')
cursor = conn.cursor()

# Execute the query to count occurrences of each message in the 403 responses
cursor.execute("SELECT MESSAGE, COUNT(*) AS Occurrences FROM threat WHERE RESPONSE = 403 GROUP BY MESSAGE")
results = cursor.fetchall()

# Print all messages and their occurrence counts
for row in results:
    message = row[0]
    occurrences = row[1]
    print(f"Message: {message} (Occurrences: {occurrences})")

# Close the database connection
cursor.close()
conn.close()
