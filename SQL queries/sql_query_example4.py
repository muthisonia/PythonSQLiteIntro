import sqlite3
from pathlib import Path

# path to the database
db_path = Path(__file__).parent.parent / "flight_management.db"

# connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# view current flight assignments for pilot 1
print("\n=== Current Flights Assigned to Pilot 1 (Anna Visser) ===")
cursor.execute("""
SELECT 
  p.pilotID, 
  p.firstName || ' ' || p.lastName AS Pilot,
  fc.role,
  f.flightID, f.flightNo, f.departure, f.arrival, f.status,
  d_from.IATA AS origin, d_to.IATA AS destination,
  fc.assignedAt
FROM FlightCrew AS fc
JOIN Pilot AS p ON fc.pilotID = p.pilotID
JOIN Flight AS f ON fc.flightID = f.flightID
JOIN Destination AS d_from ON f.originID = d_from.destinationID
JOIN Destination AS d_to   ON f.destinationID = d_to.destinationID
WHERE p.pilotID = 1
ORDER BY f.departure;
""")

rows = cursor.fetchall()
if not rows:
    print("No assigned flights found.")
else:
    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    print("-" * 115)
    for row in rows:
        print(" | ".join(str(item) for item in row))

# assign pilot 1 to flight 4 (EY104) as Captain
print("\nAssigning Pilot 1 (Anna Visser) to Flight 4 (EY104) as Captain...")
try:
    cursor.execute("""
        INSERT INTO FlightCrew (pilotID, flightID, role, assignedAt)
        VALUES (1, 4, 'Captain', datetime('now'));
    """)
    conn.commit()
    print("Pilot 1 successfully assigned to Flight 4 as Captain.")
except sqlite3.IntegrityError as e:
    print(f"Assignment failed: {e}")

# view updated schedule for pilot 1
print("\n=== Updated Flights Assigned to Pilot 1 (Anna Visser) ===")
cursor.execute("""
SELECT 
  p.pilotID, 
  p.firstName || ' ' || p.lastName AS Pilot,
  fc.role,
  f.flightID, f.flightNo, f.departure, f.arrival, f.status,
  d_from.IATA AS origin, d_to.IATA AS destination,
  fc.assignedAt
FROM FlightCrew AS fc
JOIN Pilot AS p ON fc.pilotID = p.pilotID
JOIN Flight AS f ON fc.flightID = f.flightID
JOIN Destination AS d_from ON f.originID = d_from.destinationID
JOIN Destination AS d_to   ON f.destinationID = d_to.destinationID
WHERE p.pilotID = 1
ORDER BY f.departure;
""")

rows = cursor.fetchall()
if not rows:
    print("No assigned flights found.")
else:
    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    print("-" * 115)
    for row in rows:
        print(" | ".join(str(item) for item in row))

# close connection
conn.close()
