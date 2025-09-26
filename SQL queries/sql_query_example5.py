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
print("\n=== Before Update: Destination 11 ===")
cursor.execute("""
SELECT destinationID, IATA, airportName, city, country, isActive
FROM Destination
WHERE destinationID = 11;
""")
rows = cursor.fetchall()
if not rows:
    print("Destination 11 not found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 100)
    for r in rows:
        print(" | ".join(str(x) for x in r))

# Update destination
print("\nUpdating Destination 11: set isActive = 1...")
cursor.execute("""
UPDATE Destination
SET isActive    = 1
WHERE destinationID = 11;
""")
conn.commit()


# After
print("=== After Update: Destination 11 ===")
cursor.execute("""
SELECT destinationID, IATA, airportName, city, country, isActive
FROM Destination
WHERE destinationID = 11;
""")
rows = cursor.fetchall()
if not rows:
    print("Destination 11 not found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 100)
    for r in rows:
        print(" | ".join(str(x) for x in r))


conn.close()