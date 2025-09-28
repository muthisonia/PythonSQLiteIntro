import sqlite3
from pathlib import Path

# path to the database 
db_path = Path(__file__).parent.parent / "flight_management.db"

# connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

#  get the number of flights arriving at each destination
print("\n=== Summary: Number of Flights Arriving at Each Destination ===")
cursor.execute("""
SELECT 
  d.IATA AS destination,
  d.city AS city,
  d.country AS country,
  COUNT(f.flightID) AS total_flights
FROM Destination AS d
LEFT JOIN Flight AS f ON f.destinationID = d.destinationID
GROUP BY d.destinationID, d.IATA, d.city, d.country
ORDER BY total_flights DESC, d.IATA;
""")

rows = cursor.fetchall()
if not rows:
    print("No results found.\n")
else:
    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    print("-" * 80)
    for r in rows:
        print(" | ".join(str(x) for x in r))

# close connection
conn.close()