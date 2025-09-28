# PythonSQLiteIntro

# ✈️ Flight Management System

A structured **Command-Line Interface (CLI)** built in **Python** with **SQLite**, designed to manage core airline operations such as flights, pilots, destinations, and bookings.  


> Developed as part of a university assignment.

---
## 🗂️ Project Structure

```plaintext
PythonSQLiteIntro/
├─ Classes/
│  ├─ DatabaseManager.py
│  ├─ FlightManagement.py
│  ├─ IATAValidator.py
│  └─ Utils.py
│
├─ Data/
│  └─ iataCodes.csv
│
├─ Database creation/
│  ├─ create_db.py
│  ├─ create_db.sql
│  └─ populate_db.py
│
├─ SQL queries/
│  ├─ sql_query_example1.py
│  ├─ sql_query_example2.py
│  ├─ sql_query_example3.py
│  ├─ sql_query_example4.py
│  ├─ sql_query_example5.py
│  ├─ sql_query_example6.py
│  └─ sql_query_example7.py
│
├─ flight_management.db
├─ main.py
└─ README.md
```

## 📘 Explanation of Project Structure

#### `Classes/`
Contains helper classes used across the application:

- **`DatabaseManager.py`** – Handles all database connections, queries, and transactions.  
- **`FlightManagement.py`** – Implements the main CLI logic, including all menu commands.  
- **`Utils.py`** – Provides reusable utility functions for input validation, formatting, and user interaction.  
- **`IATAValidator.py`** – Validates IATA codes using the reference list in the `Data/` folder.  

---

#### `Data/`
Stores reference data used by the application:

- **`iataCodes.csv`** – Contains a list of valid IATA codes used for input validation.  

---

#### `Database creation/`
Includes scripts for building and populating the SQLite database:

- **`create_db.sql`** – Defines the database schema (tables, constraints, relationships).  
- **`create_db.py`** – Builds the database structure by executing the SQL schema.  
- **`populate_db.py`** – Populates the database with initial sample data.  

---

#### `SQL queries/`
Contains the SQL queries used for the examples presented in the **report** submitted alongside this repository (section SQL Queries and Database Interaction).  


---

#### `flight_management.db`
The main SQLite database file containing all tables and data.  

---

#### `main.py`
The entry point of the application. Run this file to start the CLI interface.

---

#### `README.md`
The main documentation file explaining setup, usage, and project structure.



## 🚀 Getting Started
If you have already **cloned the repository** or are working in **GitHub Codespaces**, the SQLite database (`flight_management.db`) is already included in the project.  
No additional setup is required, so you can simply run the main application:

```bash
python3 main.py
```

## 🏗️ Option: Rebuild database from schema
If you would like to **recreate the database from scratch**, follow these steps:

```bash
cd "Database creation"
python3 create_db.py
python3 populate_db.py
```

## 🧑‍💻 CLI Overview

When you run main.py, you’ll see the main menu:
```
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

Choose an option:
```

You can navigate through the menu by typing the corresponding number for each command and pressing **Enter**.  


>For a detailed walkthrough of each command (including screenshots and SQL explanations), please refer to the **report** submitted alongside this repository.
