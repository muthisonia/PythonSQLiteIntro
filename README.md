# PythonSQLiteIntro

# ✈️ Flight Management System

A structured **Command-Line Interface (CLI)** built in **Python** with **SQLite**, designed to manage core airline operations such as flights, pilots, destinations, and bookings.  
The project demonstrates database design, CRUD operations, data validation, and user-friendly CLI interaction.

> 🧭 Developed as part of a university assignment to integrate SQL and Python in a real-world inspired scenario.

---

## 🗂️ Project Structure

```plaintext
PythonSQLiteIntro/
├─ Classes/
│  ├─ DatabaseManager.py
│  ├─ Utils.py
│  └─ IATAValidator.py
├─ Data/
│  └─ iataCodes.csv
├─ Database creation/
│  ├─ create_schema.sql
│  └─ populate_db.py
├─ SQL queries/
│  ├─ sql_query_example1.py
│  ├─ sql_query_example2.py
│  ├─ sql_query_example3.py
│  ├─ sql_query_example4.py
│  ├─ sql_query_example5.py
│  ├─ sql_query_example6.py
│  └─ sql_query_example7.py
├─ flight_management.db
├─ main.py
└─ README.md


## 🚀 Getting Started
🧭 Option 1: Run with pre-built database
git clone https://github.com/muthisonia/PythonSQLiteIntro.git
cd PythonSQLiteIntro
python3 main.py

## 🏗️ Option 2: Rebuild database from schema
cd "Database creation"
python3 create_db.py
python3 populate_db.py
cd ..
python3 main.py

## 🧑‍💻 CLI Overview

When you run main.py, you’ll see the main menu:

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
