import csv
from pathlib import Path

class IATAValidator:
    """Loads a list of valid IATA airport codes from a CSV file and validates user input."""

    def __init__(self, csv_path: Path):
        self.iata_codes = self._load_iata_codes(csv_path)

    def _load_iata_codes(self, csv_path: Path):
        """Load all valid IATA codes from a CSV into a dictionary."""
        iata_dict = {}
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                iata_dict[row["IATA"].strip().upper()] = {
                    "airport": row["Airport"],
                    "city": row["City"],
                    "country": row["Country"],
                }
        return iata_dict

    def is_valid(self, iata: str) -> bool:
        """Return True if IATA code exists in list."""
        return iata.upper() in self.iata_codes

    def get_info(self, iata: str):
        """Return airport info if exists, else None."""
        return self.iata_codes.get(iata.upper())

    def prompt_valid_iata(self, prompt_msg: str) -> str:
        """Prompt user repeatedly until they enter a valid IATA code."""
        while True:
            iata = input(prompt_msg).strip().upper()
            if not iata:
                print("IATA code cannot be empty.\n")
                continue

            if not self.is_valid(iata):
                print(f"'{iata}' is not a valid IATA code. Please try again.\n")
                continue

            return iata
