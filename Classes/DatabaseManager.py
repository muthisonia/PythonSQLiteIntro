import sqlite3
from datetime import datetime
from pathlib import Path
from textwrap import dedent


# Path to your database 
DB_PATH = Path(__file__).parent.parent / "flight_management.db"

# ======================================================
# Database Manager Class
# ======================================================
class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        """
        Initialize a connection to the SQLite database.
        Enable foreign key constraints.
        """
        # Connect to the database
        self.conn = sqlite3.connect(db_path)
        # To allow column access by name
        self.conn.row_factory = sqlite3.Row  
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def execute(self, sql, params=()):
        """
        Execute INSERT, UPDATE, DELETE queries and commits the transaction.
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