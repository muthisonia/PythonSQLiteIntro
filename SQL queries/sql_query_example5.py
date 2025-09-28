import sqlite3
from pathlib import Path

# path to the database
db_path = Path(__file__).parent.parent / "flight_management.db"

# connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# show destination details before update
print("\n=== Before Update: Destination 51 ===")
cursor.execute("""
SELECT destinationID, IATA, airportName, city, country, isActive
FROM Destination
WHERE destinationID = 51;
""")
rows = cursor.fetchall()
if not rows:
    print("Destination 51 not found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 100)
    for r in rows:
        print(" | ".join(str(x) for x in r))

# update destination
print("\nUpdating Destination 51: set isActive = 1...")
cursor.execute("""
UPDATE Destination
SET isActive    = 1
WHERE destinationID = 51;
""")
conn.commit()


# show destination details after update
print("=== After Update: Destination 51 ===")
cursor.execute("""
SELECT destinationID, IATA, airportName, city, country, isActive
FROM Destination
WHERE destinationID = 51;
""")
rows = cursor.fetchall()
if not rows:
    print("Destination 51 not found.\n")
else:
    cols = [d[0] for d in cursor.description]
    print(" | ".join(cols))
    print("-" * 100)
    for r in rows:
        print(" | ".join(str(x) for x in r))


conn.close()