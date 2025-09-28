import sqlite3
from datetime import datetime
from pathlib import Path
from textwrap import dedent


# Path to your database 
DB_PATH = Path(__file__).parent.parent / "flight_management.db"

# ==============================================================================
# Utility Class
# Contains helper methods for various actions such as printing or input parsing.
# ==============================================================================
class Utils:
    @staticmethod
    def header(title: str): 
        """
        Provides better headers.
        """
        bar = "=" * 70
        print("\n" + bar)
        print(title.upper().center(70))
        print(bar + "\n")

    @staticmethod
    def print_rows(rows):
        """
        Formats and prints query results in a nicer table layout.
        """
        if not rows:
            print("No results.\n")
            return
        cols = rows[0].keys()
        header = " | ".join(cols)
        print(header)
        print("-" * len(header))
        for r in rows:
            print(" | ".join(str(r[c]) if r[c] is not None else "" for c in cols))
        print()

    @staticmethod
    def input_or_blank(prompt):
        """
        Return None if user hits Enter (useful for optional updates).
        """
        s = input(prompt).strip()
        return s if s != "" else None

    @staticmethod
    def parse_int_or_none(s):
        """
        Convert to int or return None when not valid.
        """
        try:
            return int(s) if s is not None else None
        except ValueError:
            return None
        

    @staticmethod
    def prompt_valid_date(prompt_msg: str) -> str:
        """
        Prompt until user enters a valid date in YYYY-MM-DD format.
        Returns normalized string 'YYYY-MM-DD'.
        """
        while True:
            s = input(prompt_msg).strip()
            try:
                d = datetime.strptime(s, "%Y-%m-%d")
                return d.strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD (e.g., 2025-10-01)\n")


    @staticmethod
    def prompt_valid_datetime(prompt_msg: str, allow_past: bool = True) -> str:
        """Prompt until user enters a valid datetime (YYYY-MM-DD HH:MM)."""
        while True:
            s = input(prompt_msg).strip()
            try:
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
                if not allow_past and dt < datetime.now():
                    print("The date/time cannot be in the past.\n")
                    continue
                return dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid format. Use YYYY-MM-DD HH:MM (e.g., 2025-10-01 08:30)\n")

    @staticmethod
    def prompt_valid_datetime_or_blank(prompt_msg: str, allow_past: bool = True) -> str | None:
        """
        Like prompt_valid_datetime, but Enter keeps current value (returns None).
        """
        while True:
            s = input(prompt_msg).strip()
            if s == "":
                return None
            try:
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
                if not allow_past and dt < datetime.now():
                    print("The date/time cannot be in the past.\n")
                    continue
                return dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid format. Use YYYY-MM-DD HH:MM (e.g., 2025-10-01 08:30)\n")

    @staticmethod
    def prompt_valid_status_or_blank(prompt_msg: str) -> str | None:
        """
        Prompt for a valid status (Scheduled/Delayed/Cancelled).
        Enter keeps current value (returns None).
        """
        valid = {"Scheduled", "Delayed", "Cancelled"}
        while True:
            s = input(prompt_msg).strip()
            if s == "":
                return None
            s_norm = s.capitalize()
            if s_norm in valid:
                return s_norm
            print("Invalid status. Choose: Scheduled, Delayed, or Cancelled.\n")

    @staticmethod
    def flight_no_exists(db, flight_no: str) -> bool:
        """Check if a flight number exists in the Flight table."""
        rows = db.query(
            "SELECT 1 FROM Flight WHERE UPPER(flightNo) = UPPER(?) LIMIT 1;",
            (flight_no.strip(),)
        )
        return bool(rows)

    @staticmethod
    def prompt_unique_flight_no(db):
        """Prompt until the user enters a flight number not already in the DB."""
        while True:
            flight_no = input("Flight number (e.g. EY999): ").strip().upper()
            if not flight_no:
                print("Flight number cannot be empty.\n")
                continue
            if Utils.flight_no_exists(db, flight_no):
                print(f"Flight '{flight_no}' already exists. Please enter a different flight number.\n")
                continue
            return flight_no
    
    @staticmethod
    def prompt_existing_flight_no(db):
        """Prompt until the user enters a flight number that exists in the DB."""
        while True:
            flight_no = input("Flight number (e.g., EY101): ").strip().upper()
            if not flight_no:
                print("Flight number cannot be empty.\n")
                continue
            exists = db.query("SELECT 1 FROM Flight WHERE flightNo = ?;", (flight_no,))
            if not exists:
                print(f"Flight '{flight_no}' not found. Please try again.\n")
                continue
            return flight_no


    # helper lookup destination id by iata code 
    @staticmethod
    def get_destination_id_by_iata(db, iata: str):
        """Return destinationID given an IATA code, or None if not found."""
        if not iata:
            return None
        rows = db.query(
            "SELECT destinationID FROM Destination WHERE IATA = ?;",
            (iata.upper(),)
        )
        return rows[0]["destinationID"] if rows else None
    
