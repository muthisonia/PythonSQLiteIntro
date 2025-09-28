import sqlite3
from pathlib import Path

# path to the database
db_path = Path(__file__).parent.parent / "flight_management.db"

# connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# retrieve all cancelled flights to Atlanta (ATL)
print("\n=== Cancelled flights to Atlanta (ATL) ===")
cursor.execute("""
SELECT 
  f.flightNo, f.status, f.departure, f.arrival,
  d_from.IATA AS origin, d_to.IATA AS destination
FROM Flight AS f
JOIN Destination AS d_from ON f.originID = d_from.destinationID
JOIN Destination AS d_to   ON f.destinationID = d_to.destinationID
WHERE d_to.IATA = 'ATL'
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

# close connection
conn.close()