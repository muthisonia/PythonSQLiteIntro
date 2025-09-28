import sqlite3
from pathlib import Path


# path to the database
DB_PATH = Path(__file__).parent.parent / "flight_management.db"

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        """
        Initialize a database connection and enable foreign key support.
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def execute(self, sql, params=()):
        """
        Run INSERT, UPDATE, or DELETE statements and commit changes.
        """
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql, params=()):
        """
        Execute SELECT queries and return all results.
        """
        cur = self.conn.execute(sql, params)
        return cur.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()