import sqlite3
from pathlib import Path

# path to the database
db_path = Path(__file__).parent.parent / "flight_management.db"

# connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("PRAGMA foreign_keys = ON;")

#  get the number of flights assigned to each pilot
print("\n=== Summary: Number of Flights Assigned to Each Pilot ===")
cursor.execute("""
SELECT 
  p.pilotID,
  p.firstName || ' ' || p.lastName AS Pilot,
  COUNT(fc.flightID) AS total_assigned_flights
FROM Pilot AS p
LEFT JOIN FlightCrew AS fc ON fc.pilotID = p.pilotID
GROUP BY p.pilotID, p.firstName, p.lastName
ORDER BY total_assigned_flights DESC, p.pilotID;
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