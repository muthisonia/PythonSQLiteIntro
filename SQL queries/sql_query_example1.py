import sqlite3
from pathlib import Path

# Path to your database 
db_path = Path(__file__).parent.parent / "flight_management.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

#  Retrieve all cancelled flights to Amsterdam Schiphol (AMS)
print("\n=== Cancelled flights to Amsterdam Schiphol (AMS) ===")
cursor.execute("""
SELECT 
  f.flightNo, f.status, f.departure, f.arrival,
  d_from.IATA AS origin, d_to.IATA AS destination
FROM Flight AS f
JOIN Destination AS d_from ON f.originID = d_from.destinationID
JOIN Destination AS d_to   ON f.destinationID = d_to.destinationID
WHERE d_to.IATA = 'AMS'
  AND f.status = 'Cancelled'
ORDER BY f.departure;
""")
rows = cursor.fetchall()

if not rows:
    print("No results found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 90)
    for r in rows:
        print(" | ".join(str(x) for x in r))
    print()

# Close connection
conn.close()