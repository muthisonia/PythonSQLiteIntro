-- This is used to enable the enforcement of foreign key
PRAGMA foreign_keys = ON;

-- 1. DESTINATION TABLE
CREATE TABLE Destination (
  destinationID INTEGER PRIMARY KEY,
  IATA          TEXT UNIQUE NOT NULL,
  airportName   TEXT NOT NULL,
  country       TEXT NOT NULL,
  city          TEXT NOT NULL,
  isActive      INTEGER NOT NULL DEFAULT 1  -- 1 = active, 0 = inactive
);


-- 2. PILOT TABLE
CREATE TABLE Pilot (
  pilotID     INTEGER PRIMARY KEY,
  firstName   TEXT NOT NULL,
  lastName    TEXT NOT NULL,
  licenseNo   TEXT UNIQUE NOT NULL,
  dateOfBirth DATE,
  rank        TEXT NOT NULL, -- e.g. Captain, Co-Captain
  email       TEXT UNIQUE,
  hireDate    DATE NOT NULL
);


-- 3. FLIGHT TABLE
CREATE TABLE Flight (
  flightID       INTEGER PRIMARY KEY,
  flightNo       TEXT UNIQUE NOT NULL,
  originID       INTEGER NOT NULL,
  destinationID  INTEGER NOT NULL,
  departure      DATETIME NOT NULL,
  arrival        DATETIME NOT NULL,
  status         TEXT NOT NULL DEFAULT 'Scheduled'
                  CHECK (status IN ('Scheduled', 'Delayed', 'Cancelled')),
  aircraft       TEXT,
  lastUpdate     DATETIME DEFAULT (datetime('now')),
  
  -- Foreign Keys
  FOREIGN KEY (originID) 
      REFERENCES Destination(destinationID)
      ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (destinationID) 
      REFERENCES Destination(destinationID)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  -- Check constraints
  CHECK (arrival > departure),
  CHECK (originID <> destinationID)
);


-- 4. FLIGHTCREW TABLE
CREATE TABLE FlightCrew (
  flightCrewID INTEGER PRIMARY KEY,
  pilotID      INTEGER NOT NULL,
  flightID     INTEGER NOT NULL,
  role         TEXT NOT NULL
                CHECK (role IN ('Captain','Co-Captain')),
  assignedAt   DATETIME DEFAULT (datetime('now')),

  -- Prevent duplicate assignments
  UNIQUE (pilotID, flightID),

  -- Foreign Keys
  FOREIGN KEY (pilotID)
      REFERENCES Pilot(pilotID)
      ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (flightID)
      REFERENCES Flight(flightID)
      ON UPDATE CASCADE ON DELETE CASCADE
);


-- 5. BOOKING TABLE
CREATE TABLE Booking (
  bookingID   INTEGER PRIMARY KEY,
  flightID    INTEGER NOT NULL,
  firstName   TEXT NOT NULL,
  lastName    TEXT NOT NULL,
  email       TEXT,
  seatNo      TEXT,
  status      TEXT NOT NULL DEFAULT 'Booked'
              CHECK (status IN ('Booked','Checked-in','Cancelled')),
  lastUpdate  DATETIME DEFAULT (datetime('now')),

  -- Prevent double-booking a seat
  UNIQUE (flightID, seatNo),

  -- Foreign Key
  FOREIGN KEY (flightID)
      REFERENCES Flight(flightID)
      ON UPDATE CASCADE ON DELETE CASCADE
);

