import sqlite3
from pathlib import Path

# define path to save create the db outside the "Database creation" folder
db_path = Path(__file__).parent.parent / "flight_management.db"

# connect to or create the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# read and execute the SQL file with the SQL queries for table creation
sql_file = Path(__file__).parent / "create_db.sql"
with open(sql_file, "r") as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.commit()
conn.close()

print(f"The database was created successfully!")
