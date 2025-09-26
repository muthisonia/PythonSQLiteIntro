import sqlite3
from pathlib import Path

# Path to your database 
db_path = Path(__file__).parent.parent / "flight_management.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Before update
print("\n=== Before Update: EY102 ===")
cursor.execute("""
SELECT 
  f.flightNo, f.status, f.departure, f.arrival,
  d_from.IATA AS origin, d_to.IATA AS destination, f.lastUpdate
FROM Flight AS f
JOIN Destination AS d_from ON f.originID = d_from.destinationID
JOIN Destination AS d_to   ON f.destinationID = d_to.destinationID
WHERE f.flightNo = 'EY102';
""")
rows = cursor.fetchall()
if not rows:
    print("No flight found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 100)
    for r in rows:
        print(" | ".join(str(x) for x in r))

# Update: delay by 2 hours and set status Delayed 
print("\nApplying 2-hour delay and setting status to 'Delayed' for EY102...")
cursor.execute("""
UPDATE Flight
SET departure  = datetime(departure, '+2 hours'),
    arrival    = datetime(arrival,   '+2 hours'),
    status     = 'Delayed',
    lastUpdate = datetime('now')
WHERE flightNo = 'EY102';
""")
conn.commit()

# After update
print("=== After Update: EY102 ===")
cursor.execute("""
SELECT 
  f.flightNo, f.status, f.departure, f.arrival,
  d_from.IATA AS origin, d_to.IATA AS destination, f.lastUpdate
FROM Flight AS f
JOIN Destination AS d_from ON f.originID = d_from.destinationID
JOIN Destination AS d_to   ON f.destinationID = d_to.destinationID
WHERE f.flightNo = 'EY102';
""")
rows = cursor.fetchall()
if not rows:
    print("No flight found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 100)
    for r in rows:
        print(" | ".join(str(x) for x in r))
        
# Close connection
conn.close()
