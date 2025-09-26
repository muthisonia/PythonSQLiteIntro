import sqlite3
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from Classes.DatabaseManager import DatabaseManager
from Classes.Utils import Utils
from Classes.IATAValidator import IATAValidator

# Path to your database 
DB_PATH = Path(__file__).parent.parent / "flight_management.db"

class FlightManagementApp:
    """Main CLI logic: all six menu operations."""
    
    def __init__(self):
        self.db = DatabaseManager(DB_PATH)
        self.iata_validator = IATAValidator(Path(__file__).parent.parent / "Data" / "iataCodes.csv")

    # helper to check if the flight number already exists
    def flight_no_exists(self, flight_no: str) -> bool:
        """Check existence check for a flight number."""
        rows = self.db.query(
            "SELECT 1 FROM Flight WHERE UPPER(flightNo) = UPPER(?) LIMIT 1;",
            (flight_no.strip(),)
        )
        return bool(rows)

    def prompt_unique_flight_no(self) -> str:
        """Prompt until the user enters a flight number not already in the DB."""
        while True:
            flight_no = input("Flight number (e.g. EY999): ").strip().upper()
            if not flight_no:
                print("Flight number cannot be empty.\n")
                continue
            if self.flight_no_exists(flight_no):
                print(f"Flight '{flight_no}' already exists. Please enter a different flight number.\n")
                continue
            return flight_no
    
    def prompt_existing_flight_no(self) -> str:
        """Prompt until the user enters a flight number that exists in the DB."""
        while True:
            flight_no = input("Flight number (e.g., EY101): ").strip().upper()
            if not flight_no:
                print("Flight number cannot be empty.\n")
                continue
            exists = self.db.query("SELECT 1 FROM Flight WHERE flightNo = ?;", (flight_no,))
            if not exists:
                print(f"Flight '{flight_no}' not found. Please try again.\n")
                continue
            return flight_no


    # helper lookup destination id by iata code
    def get_destination_id_by_iata(self, iata):
        if not iata: return None
        rows = self.db.query("SELECT destinationID FROM Destination WHERE IATA = ?", (iata.upper(),))
        return rows[0]["destinationID"] if rows else None

    # helper lookup flight id by flight no
    def get_flight_id_by_flightno(self, flight_no):
        if not flight_no: return None
        rows = self.db.query("SELECT flightID FROM Flight WHERE flightNo = ?", (flight_no,))
        return rows[0]["flightID"] if rows else None
    
    def prompt_valid_iata(self, prompt_msg):
        """Prompt user for a valid IATA code that exists in the Destination table."""
        while True:
            iata = input(prompt_msg).strip().upper()
            if not iata:
                print("IATA code cannot be empty.\n")
                continue

            dest_id = self.get_destination_id_by_iata(iata)
            if dest_id is None:
                print(f"'{iata}' not found in Destination table. Please try again.\n")
                continue
            return iata

    # 1) Function to add a new flight
    def add_new_flight(self):
        Utils.header("Add a New Flight")

        #  flight no
        flight_no = self.prompt_unique_flight_no()

        # origin iata
        origin_iata = self.iata_validator.prompt_valid_iata("Origin IATA: ")

        # destination iata
        while True:
            dest_iata = self.iata_validator.prompt_valid_iata("Destination IATA: ")
            if dest_iata == origin_iata:
                print("Destination cannot be the same as Origin. Please choose another airport.\n")
                continue
            break

        # Look up their corresponding IDs in the Destination table
        origin_id = self.get_destination_id_by_iata(origin_iata)
        dest_id   = self.get_destination_id_by_iata(dest_iata)

        # departure and arrival
        departure = Utils.prompt_valid_datetime("Departure (YYYY-MM-DD HH:MM): ")
        dep_dt = datetime.strptime(departure, "%Y-%m-%d %H:%M")

        while True:
            arrival = Utils.prompt_valid_datetime("Arrival (YYYY-MM-DD HH:MM): ")
            arr_dt = datetime.strptime(arrival, "%Y-%m-%d %H:%M")

            if arr_dt <= dep_dt:
                print("Arrival time must be after departure time. Please try again.\n")
                continue
            break

        
        # status
        valid_statuses = ["Scheduled", "Delayed", "Cancelled"]
        while True:
            status_input = Utils.input_or_blank("Status [Scheduled/Delayed/Cancelled] (default Scheduled): ")
            if not status_input:
                status = "Scheduled"
                break
            status_input = status_input.capitalize()
            if status_input not in valid_statuses:
                print(f"Invalid status. Please choose one of: {', '.join(valid_statuses)}.\n")
                continue
            status = status_input
            break

        aircraft = Utils.input_or_blank("Aircraft: ")

        # Show summary before inserting
        print("\nPlease confirm the flight details:")
        print(f"  Flight No:     {flight_no}")
        print(f"  Origin:        {origin_iata}")
        print(f"  Destination:   {dest_iata}")
        print(f"  Departure:     {departure}")
        print(f"  Arrival:       {arrival}")
        print(f"  Status:        {status}")
        print(f"  Aircraft:      {aircraft or '(none)'}")
        print()

        # Confirm action
        while True:
            confirm = input("Do you want to add this flight? (Y/N): ").strip().upper()
            if confirm == "Y":
                break
            elif confirm == "N":
                print("Operation cancelled. Returning to main menu.\n")
                return
            else:
                print("Please enter Y or N.\n")

        try:
            self.db.execute(dedent("""
                INSERT INTO Flight (flightNo, originID, destinationID, departure, arrival, status, aircraft, lastUpdate)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'));
            """), (flight_no, origin_id, dest_id, departure, arrival, status, aircraft))
            print(f"Flight {flight_no} added.\n")
        except Exception as e:
            print(f"Error: {e}\n")

    # 2) Function to view flights by criteria
    def view_flights_by_criteria(self):
        Utils.header("View Flights by Criteria")

        # --- Show filter menu ---
        print("Choose one or more filters (comma-separated), or press Enter for none:")
        print("  1) Destination IATA")
        print("  2) Origin IATA")
        print("  3) Status (Scheduled / Delayed / Cancelled)")
        print("  4) Departure Date (YYYY-MM-DD)")

        # --- Loop until valid input ---
        chosen = set()
        while True:
            choice = input("Filters to apply (e.g., 1,3,4): ").strip()
            if not choice:
                # no filters
                break

            # Split by comma and clean tokens
            tokens = [t.strip() for t in choice.split(",") if t.strip()]
            valid = {"1", "2", "3", "4"}
            invalid_tokens = [t for t in tokens if t not in valid]

            if invalid_tokens:
                print(f"Invalid selections: {', '.join(invalid_tokens)}. Use digits 1-4 separated by commas.\n")
                continue
            if len(tokens) != len(set(tokens)):
                print("Duplicate numbers detected. Please list each filter only once.\n")
                continue

            # All good
            chosen = {int(t) for t in tokens}
            break

        # --- Prepare inputs ---
        dest_iata = origin_iata = status = dep_date = None

        if 1 in chosen:
            dest_iata = self.iata_validator.prompt_valid_iata("Destination IATA: ")
        if 2 in chosen:
            origin_iata = self.iata_validator.prompt_valid_iata("Origin IATA: ")
        if 3 in chosen:
            valid_statuses = {"Scheduled", "Delayed", "Cancelled"}
            while True:
                s = input("Status [Scheduled/Delayed/Cancelled]: ").strip().capitalize()
                if s in valid_statuses:
                    status = s
                    break
                print("Invalid status. Choose: Scheduled, Delayed, or Cancelled.\n")
        if 4 in chosen:
            dep_date = Utils.prompt_valid_date("Departure date (YYYY-MM-DD): ")

        # --- Build SQL dynamically ---
        base_sql = """
            SELECT 
            f.flightNo, f.status, f.departure, f.arrival,
            o.IATA AS origin, d.IATA AS destination
            FROM Flight f
            JOIN Destination o ON f.originID = o.destinationID
            JOIN Destination d ON f.destinationID = d.destinationID
            WHERE 1=1
        """
        conditions = []
        params = {}

        if dest_iata:
            conditions.append("AND d.IATA = :dest_iata")
            params["dest_iata"] = dest_iata
        if origin_iata:
            conditions.append("AND o.IATA = :origin_iata")
            params["origin_iata"] = origin_iata
        if status:
            conditions.append("AND f.status = :status")
            params["status"] = status
        if dep_date:
            conditions.append("AND date(f.departure) = :dep_date")
            params["dep_date"] = dep_date

        sql = base_sql + "\n".join(conditions) + "\nORDER BY f.departure;"

        rows = self.db.query(sql, params)
        Utils.print_rows(rows)


    # 3) Function to update flight information
    def update_flight_information(self):
        Utils.header("Update Flight Information")

        # check if the flight number exists in the database
        while True:
            flight_no = input("Flight number to update (e.g., EY101): ").strip().upper()
            if not flight_no:
                print("Flight number cannot be empty.\n")
                continue
            # Check existence
            exists = self.db.query("SELECT 1 FROM Flight WHERE flightNo = ?;", (flight_no,))
            if not exists:
                print(f"Flight '{flight_no}' does not exist. Please try again.\n")
                continue
            break

        current = self.db.query(dedent("""
            SELECT f.flightNo, f.status, f.departure, f.arrival, f.aircraft,
                   o.IATA AS origin, d.IATA AS destination, f.lastUpdate
            FROM Flight f
            JOIN Destination o ON f.originID = o.destinationID
            JOIN Destination d ON f.destinationID = d.destinationID
            WHERE f.flightNo = ?;
        """), (flight_no,))
        if not current:
            print("Flight not found.\n")
            return
        print("\n")
        Utils.print_rows(current)

        print("leave fields blank to keep existing values.\n")
        new_departure = Utils.prompt_valid_datetime_or_blank("New departure (YYYY-MM-DD HH:MM): ", allow_past=False)
        new_arrival   = Utils.prompt_valid_datetime_or_blank("New arrival   (YYYY-MM-DD HH:MM): ", allow_past=False)
        new_status    = Utils.prompt_valid_status_or_blank("New status [Scheduled/Delayed/Cancelled]: ")
        new_aircraft  = Utils.input_or_blank("New aircraft: ")


        # Show summary before inserting
        print("\nPlease confirm the flight details:")
        print(f"  Flight No: {flight_no}")
        print(f"  Departure: {new_departure}")
        print(f"  Arrival:   {new_arrival}")
        print(f"  Status:    {new_status}")
        print(f"  Aircraft:  {new_aircraft}")
        print()

        # Confirm action
        while True:
            confirm = input("Do you want to modify flight? (Y/N): ").strip().upper()
            if confirm == "Y":
                break
            elif confirm == "N":
                print("Operation cancelled. Returning to main menu.\n")
                return
            else:
                print("Please enter Y or N.\n")

        try:
            self.db.execute(dedent("""
                UPDATE Flight
                SET departure  = COALESCE(?, departure),
                    arrival    = COALESCE(?, arrival),
                    status     = COALESCE(?, status),
                    aircraft   = COALESCE(?, aircraft),
                    lastUpdate = datetime('now')
                WHERE flightNo = ?;
            """), (new_departure, new_arrival, new_status, new_aircraft, flight_no))
            print("Flight updated.\n")
        except sqlite3.IntegrityError as e:
            print(f"Update failed: {e}\n")
            return

        updated = self.db.query(dedent("""
            SELECT f.flightNo, f.status, f.departure, f.arrival, f.aircraft,
                   o.IATA AS origin, d.IATA AS destination, f.lastUpdate
            FROM Flight f
            JOIN Destination o ON f.originID = o.destinationID
            JOIN Destination d ON f.destinationID = d.destinationID
            WHERE f.flightNo = ?;
        """), (flight_no,))
        Utils.print_rows(updated)

    # 4) Function to assign pilot to flight
    def assign_pilot_to_flight(self):
        Utils.header("Assign Pilot to Flight")

        # validate pilot ID
        while True:
            pilot_id = Utils.parse_int_or_none(Utils.input_or_blank("Pilot ID (e.g., 1): "))
            if pilot_id is None:
                print("Invalid pilot ID.\n")
                continue

            # check existence in Pilot table
            pilot_exists = self.db.query("SELECT firstName || ' ' || lastName AS name FROM Pilot WHERE pilotID = ?;", (pilot_id,))
            if not pilot_exists:
                print(f"Pilot with ID {pilot_id} not found in database.\n")
                continue

            pilot_name = pilot_exists[0]["name"]
            print(f"Found Pilot: {pilot_name}")
            break

        # validate flight number
        while True:
            flight_no = input("Flight number (e.g., EY104): ").strip().upper()
            if not flight_no:
                print("Flight number cannot be empty.\n")
                continue
            flight_id = self.get_flight_id_by_flightno(flight_no)
            if flight_id is None:
                print(f"Flight '{flight_no}' not found.\n")
                continue
            break

        # validate role
        valid_roles = ("Captain", "Co-Captain")
        while True:
            role = (Utils.input_or_blank("Role [Captain/Co-Captain] (default Captain): ") or "Captain").title()
            if role not in valid_roles:
                print("Role must be 'Captain' or 'Co-Captain'. Please try again.\n")
                continue
            break

        # confirm before assignment
        print("\nYou are about to assign:")
        print(f"  Pilot: {pilot_name} (ID: {pilot_id})")
        print(f"  Flight: {flight_no}")
        print(f"  Role: {role}")
        print("\n")
        confirm = input("Confirm assignment? (Y/N): ").strip().upper()
        if confirm != "Y":
            print("Assignment cancelled.\n")
            return
        
        # check if pilot already assigned to this flight
        exists = self.db.query("""
            SELECT 1 FROM FlightCrew
            WHERE pilotID = ? AND flightID = ?;
        """, (pilot_id, flight_id))

        if exists:
            print(f"Pilot {pilot_name} (ID: {pilot_id}) is already assigned to flight {flight_no}.\n")
            return

        try:
            self.db.execute(
                "INSERT INTO FlightCrew (pilotID, flightID, role, assignedAt) VALUES (?, ?, ?, datetime('now'));",
                (pilot_id, flight_id, role),
            )
            print(f"Assigned pilot {pilot_name} (ID: {pilot_id}) to flight {flight_no} as {role}.\n")
        except sqlite3.IntegrityError as e:
            print(f"Assignment failed: {e}\n")
            return

        # show pilot's updated schedule
        self._show_pilot_schedule(pilot_id)

    # 5) Function to view pilot schedule
    def view_pilot_schedule(self):
        Utils.header("View Pilot Schedule")

        # validate pilot ID
        while True:
            pilot_id = Utils.parse_int_or_none(Utils.input_or_blank("Pilot ID (e.g., 1): "))
            if pilot_id is None:
                print("Invalid pilot ID.\n")
                continue

            # vheck existence in Pilot table
            pilot_exists = self.db.query("SELECT firstName || ' ' || lastName AS name FROM Pilot WHERE pilotID = ?;", (pilot_id,))
            if not pilot_exists:
                print(f"Pilot with ID {pilot_id} not found in database.\n")
                continue

            pilot_name = pilot_exists[0]["name"]
            print(f"Found Pilot: {pilot_name}")
            print("\n")
            break

        self._show_pilot_schedule(pilot_id)

    def _show_pilot_schedule(self, pilot_id: int):
        rows = self.db.query(dedent("""
            SELECT 
              p.pilotID,
              p.firstName || ' ' || p.lastName AS Pilot,
              fc.role,
              f.flightNo, f.departure, f.arrival, f.status,
              o.IATA AS origin, d.IATA AS destination,
              fc.assignedAt
            FROM FlightCrew fc
            JOIN Pilot p  ON fc.pilotID = p.pilotID
            JOIN Flight f ON fc.flightID = f.flightID
            JOIN Destination o ON f.originID = o.destinationID
            JOIN Destination d ON f.destinationID = d.destinationID
            WHERE p.pilotID = ?
            ORDER BY f.departure;
        """), (pilot_id,))
        Utils.print_rows(rows)

    # 6) Function to view/update destination information
    def view_update_destination(self):
        Utils.header("View/Update Destination Information")
        print("1) View active destinations")
        print("2) View all destinations")
        print("3) Update a destination")
        print()
        choice = input("Choose: ").strip()

        if choice == "1":
            rows = self.db.query(dedent("""
                SELECT destinationID, IATA, airportName, city, country, isActive
                FROM Destination
                WHERE isActive = 1
                ORDER BY destinationID;
            """))
            Utils.print_rows(rows)
            return

        if choice == "2":
            rows = self.db.query(dedent("""
                SELECT destinationID, IATA, airportName, city, country, isActive
                FROM Destination
                ORDER BY destinationID;
            """))
            Utils.print_rows(rows)
            return

        
        if choice == "3":
            # pick an existing destination
            while True:
                dest_id = Utils.parse_int_or_none(Utils.input_or_blank("Destination ID to update: "))
                if dest_id is None:
                    print("Invalid ID.\n")
                    continue
                current = self.db.query("SELECT * FROM Destination WHERE destinationID = ?;", (dest_id,))
                if not current:
                    print("Destination not found.\n")
                    continue
                break

            # show current record
            Utils.print_rows(current)
            row = current[0]

            while True:
                new_active = Utils.input_or_blank("Set isActive [1=active / 0=inactive]: ")
                if new_active in ("0", "1"):
                    active_val = int(new_active)
                    break
                print("Please enter 1 (active) or 0 (inactive).\n")

            # no change check
            if active_val == row["isActive"]:
                print("ℹNo change detected (isActive unchanged).")
                return

            # confirm
            print("\nYou are about to update this destination:")
            print(f"  destinationID: {dest_id}")
            print(f"  IATA:          {row['IATA']}")
            print(f"  airportName:   {row['airportName']}")
            print(f"  city/country:  {row['city']}, {row['country']}")
            print(f"  isActive:      {row['isActive']} -> {active_val}")
            while True:
                confirm = input("\nConfirm update? (Y/N): ").strip().upper()
                if confirm in ("Y", "N"):
                    break
                print("Please enter Y or N.\n")
            if confirm == "N":
                print("Update cancelled.\n")
                return

            try:
                self.db.execute(
                    "UPDATE Destination SET isActive = ? WHERE destinationID = ?;",
                    (active_val, dest_id)
                )
                print("Destination updated.\n")
            except sqlite3.IntegrityError as e:
                print(f"Update failed: {e}\n")
                return

            # Show after
            updated = self.db.query("SELECT * FROM Destination WHERE destinationID = ?;", (dest_id,))
            Utils.print_rows(updated)
            return

        print("Unknown choice.\n")

    # Additional command 7) Check Booking for a Flight
    def check_bookings_for_flight(self):
        Utils.header("Check Bookings for a Flight")

        #  flight no
        flight_no = self.prompt_existing_flight_no()

        # get flight details
        flight = self.db.query(dedent("""
            SELECT f.flightID, f.flightNo,
                o.IATA AS origin, d.IATA AS destination,
                f.departure
            FROM Flight f
            JOIN Destination o ON f.originID = o.destinationID
            JOIN Destination d ON f.destinationID = d.destinationID
            WHERE f.flightNo = ?;
        """), (flight_no,))[0]

        flight_id = flight["flightID"]

        # total bookings for this flight
        total_rows = self.db.query(
            "SELECT COUNT(*) AS total_bookings FROM Booking WHERE flightID = ?;",
            (flight_id,)
        )
        total = total_rows[0]["total_bookings"] if total_rows else 0

        # status breakdown (Booked / Checked-in / Cancelled)
        breakdown = self.db.query(dedent("""
            SELECT status, COUNT(*) AS cnt
            FROM Booking
            WHERE flightID = ?
            GROUP BY status
            ORDER BY status;
        """), (flight_id,))

        print("\nFlight summary:")
        print(f"  Flight:      {flight['flightNo']}  ({flight['origin']} → {flight['destination']})")
        print(f"  Departure:   {flight['departure']}")
        print(f"  Bookings:    {total}\n")

        if breakdown:
            print("By status:")
            Utils.print_rows(breakdown)
        else:
            print("No bookings found for this flight.\n")

    # Run main menu 
    def run(self):
        try:
            while True:
                print(dedent("""
                ==============================
                     Flight Management CLI
                ==============================
                1) Add a New Flight
                2) View Flights by Criteria
                3) Update Flight Information
                4) Assign Pilot to Flight
                5) View Pilot Schedule
                6) View/Update Destination Information
                7) Check Bookings for a Flight
                0) Exit
                             
                Press CTRL + C / Control + C anytime to exit.
                """))
                choice = input("Choose an option: ").strip()
                if choice == "1": self.add_new_flight()
                elif choice == "2": self.view_flights_by_criteria()
                elif choice == "3": self.update_flight_information()
                elif choice == "4": self.assign_pilot_to_flight()
                elif choice == "5": self.view_pilot_schedule()
                elif choice == "6": self.view_update_destination()
                elif choice == "7": self.check_bookings_for_flight()
                elif choice == "0":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option.\n")
        finally:
            self.db.close()