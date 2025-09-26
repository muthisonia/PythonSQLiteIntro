import sqlite3
from pathlib import Path

# Path to the existing database
db_path = Path(__file__).parent.parent / "flight_management.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Wrap inserts in a transaction
cursor.executescript("""
BEGIN TRANSACTION;


-- DESTINATION
INSERT INTO Destination (destinationID, IATA, airportName, country, city, isActive) VALUES
(1, 'ATL', 'Hartsfield–Jackson Atlanta International Airport', 'United States', 'Atlanta', 1),
(2, 'PEK', 'Beijing Capital International Airport', 'China', 'Beijing', 1),
(3, 'LAX', 'Los Angeles International Airport', 'United States', 'Los Angeles', 1),
(4, 'DXB', 'Dubai International Airport', 'United Arab Emirates', 'Dubai', 1),
(5, 'HND', 'Tokyo Haneda Airport', 'Japan', 'Tokyo', 1),
(6, 'ORD', 'Chicago O''Hare International Airport', 'United States', 'Chicago', 1),
(7, 'LHR', 'London Heathrow Airport', 'United Kingdom', 'London', 1),
(8, 'HKG', 'Hong Kong International Airport', 'China', 'Hong Kong', 1),
(9, 'PVG', 'Shanghai Pudong International Airport', 'China', 'Shanghai', 1),
(10, 'CDG', 'Paris Charles de Gaulle Airport', 'France', 'Paris', 1),
(11, 'DFW', 'Dallas/Fort Worth International Airport', 'United States', 'Dallas', 1),
(12, 'CAN', 'Guangzhou Baiyun International Airport', 'China', 'Guangzhou', 1),
(13, 'AMS', 'Amsterdam Schiphol Airport', 'Netherlands', 'Amsterdam', 1),
(14, 'FRA', 'Frankfurt am Main Airport', 'Germany', 'Frankfurt', 1),
(15, 'IST', 'Istanbul Airport', 'Turkey', 'Istanbul', 1),
(16, 'DEL', 'Indira Gandhi International Airport', 'India', 'Delhi', 1),
(17, 'SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore', 1),
(18, 'ICN', 'Incheon International Airport', 'South Korea', 'Seoul', 1),
(19, 'BKK', 'Suvarnabhumi Airport', 'Thailand', 'Bangkok', 1),
(20, 'DEN', 'Denver International Airport', 'United States', 'Denver', 1),
(21, 'JFK', 'John F. Kennedy International Airport', 'United States', 'New York', 1),
(22, 'KUL', 'Kuala Lumpur International Airport', 'Malaysia', 'Kuala Lumpur', 1),
(23, 'MAD', 'Madrid Barajas Airport', 'Spain', 'Madrid', 1),
(24, 'SFO', 'San Francisco International Airport', 'United States', 'San Francisco', 1),
(25, 'LAS', 'Harry Reid International Airport', 'United States', 'Las Vegas', 1),
(26, 'BCN', 'Barcelona–El Prat Airport', 'Spain', 'Barcelona', 1),
(27, 'YYZ', 'Toronto Pearson International Airport', 'Canada', 'Toronto', 1),
(28, 'MUC', 'Franz Josef Strauss International Airport', 'Germany', 'Munich', 1),
(29, 'MCO', 'Orlando International Airport', 'United States', 'Orlando', 1),
(30, 'SEA', 'Seattle–Tacoma International Airport', 'United States', 'Seattle', 1),
(31, 'MIA', 'Miami International Airport', 'United States', 'Miami', 1),
(32, 'FCO', 'Rome Fiumicino Airport', 'Italy', 'Rome', 1),
(33, 'EWR', 'Newark Liberty International Airport', 'United States', 'Newark', 1),
(34, 'GRU', 'São Paulo–Guarulhos International Airport', 'Brazil', 'São Paulo', 1),
(35, 'CLT', 'Charlotte Douglas International Airport', 'United States', 'Charlotte', 1),
(36, 'PHX', 'Phoenix Sky Harbor International Airport', 'United States', 'Phoenix', 1),
(37, 'IAH', 'George Bush Intercontinental Airport', 'United States', 'Houston', 1),
(38, 'MEL', 'Melbourne Airport', 'Australia', 'Melbourne', 1),
(39, 'SYD', 'Sydney Kingsford Smith Airport', 'Australia', 'Sydney', 1),
(40, 'BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'India', 'Mumbai', 1),
(41, 'BOS', 'Logan International Airport', 'United States', 'Boston', 1),
(42, 'NRT', 'Narita International Airport', 'Japan', 'Tokyo', 1),
(43, 'SVO', 'Sheremetyevo International Airport', 'Russia', 'Moscow', 1),
(44, 'LIS', 'Humberto Delgado Airport', 'Portugal', 'Lisbon', 1),
(45, 'ZRH', 'Zurich Airport', 'Switzerland', 'Zurich', 1),
(46, 'VIE', 'Vienna International Airport', 'Austria', 'Vienna', 1),
(47, 'DOH', 'Hamad International Airport', 'Qatar', 'Doha', 1),
(48, 'ATH', 'Athens International Airport', 'Greece', 'Athens', 1),
(49, 'CPH', 'Copenhagen Airport', 'Denmark', 'Copenhagen', 1),
(50, 'OSL', 'Oslo Gardermoen Airport', 'Norway', 'Oslo', 1),
(51, 'BAY', 'Maramureș International Airport', 'Romania', 'Baia Mare', 0);



-- PILOT
INSERT INTO Pilot (pilotID, firstName, lastName, licenseNo, dateOfBirth, email, hireDate) VALUES
(1, 'Anna',   'Visser',    'P-1001', '1980-03-11', 'anna.visser@air.example',   '2010-06-01'),
(2, 'Mark',   'Smit',      'P-1002', '1983-07-22', 'mark.smit@air.example',     '2012-03-15'),
(3, 'Luc',    'Dubois',    'P-1003', '1979-11-05', 'luc.dubois@air.example',    '2009-09-20'),
(4, 'Emily',  'Clark',     'P-1004', '1986-02-14', 'emily.clark@air.example',   '2014-01-10'),
(5, 'Jasper', 'De Jong',   'P-1005', '1982-12-30', 'jasper.dejong@air.example', '2011-08-12'),
(6, 'Sara',   'Rossi',     'P-1006', '1987-05-09', 'sara.rossi@air.example',    '2015-05-05'),
(7, 'Paul',   'Müller',    'P-1007', '1978-09-18', 'paul.mueller@air.example',  '2008-07-07'),
(8, 'Chloe',  'Martin',    'P-1008', '1990-01-28', 'chloe.martin@air.example',  '2016-10-03'),
(9, 'David',  'Brown',     'P-1009', '1984-04-17', 'david.brown@air.example',   '2012-09-01'),
(10,'Iris',   'van Dijk',  'P-1010', '1989-08-08', 'iris.vandijk@air.example',  '2017-02-21'),
(11,'Omar',   'Hassan',    'P-1011', '1981-06-04', 'omar.hassan@air.example',   '2010-11-11'),
(12,'Nina',   'Kaya',      'P-1012', '1991-10-12', 'nina.kaya@air.example',     '2018-04-30');


-- FLIGHT 
INSERT INTO Flight (flightID, flightNo, originID, destinationID, departure, arrival, status, aircraft) VALUES
(1,  'EY101', 1, 2,  '2025-10-01 08:00', '2025-10-01 09:00', 'Scheduled', 'A320'),
(2,  'EY102', 1, 3,  '2025-10-01 10:00', '2025-10-01 11:20', 'Scheduled', 'A320'),
(3,  'EY103', 2, 1,  '2025-10-01 12:00', '2025-10-01 14:15', 'Delayed',   'B737'),
(4,  'EY104', 3, 4,  '2025-10-01 09:30', '2025-10-01 10:45', 'Scheduled', 'A319'),
(5,  'EY105', 4, 5,  '2025-10-01 13:00', '2025-10-01 21:30', 'Scheduled', 'A330'),
(6,  'EY106', 5, 1,  '2025-10-01 22:30', '2025-10-02 10:30', 'Delayed',   'B787'),
(7,  'EY107', 6, 7,  '2025-10-01 07:15', '2025-10-01 09:30', 'Scheduled', 'A320'),
(8,  'EY108', 7, 8,  '2025-10-01 11:00', '2025-10-01 13:00', 'Scheduled', 'A321'),
(9,  'EY109', 8, 9,  '2025-10-01 15:00', '2025-10-01 20:30', 'Scheduled', 'A321'),
(10, 'EY110', 9, 10, '2025-10-01 09:00', '2025-10-01 11:30', 'Scheduled', 'B737'),
(11, 'EY111',10, 1,  '2025-10-01 14:00', '2025-10-01 17:30', 'Cancelled', 'A320'),
(12, 'EY112',1, 6,  '2025-10-01 18:00', '2025-10-01 20:30', 'Scheduled', 'A320');


-- FLIGHTCREW 
INSERT INTO FlightCrew (flightCrewID, pilotID, flightID, role, assignedAt) VALUES
(1, 1,  1,  'Captain',    '2025-09-25 09:00'),
(2, 2,  1,  'Co-Captain', '2025-09-25 09:00'),
(3, 3,  2,  'Captain',    '2025-09-25 09:10'),
(4, 4,  2,  'Co-Captain', '2025-09-25 09:10'),
(5, 5,  3,  'Captain',    '2025-09-25 09:20'),
(6, 6,  3,  'Co-Captain', '2025-09-25 09:20'),
(7, 7,  4,  'Captain',    '2025-09-25 09:30'),
(8, 8,  4,  'Co-Captain', '2025-09-25 09:30'),
(9, 9,  5,  'Captain',    '2025-09-25 09:40'),
(10,10, 5,  'Co-Captain', '2025-09-25 09:40'),
(11,11, 6,  'Captain',    '2025-09-25 09:50'),
(12,12, 6,  'Co-Captain', '2025-09-25 09:50'),
(13,1,  7,  'Captain',    '2025-09-25 10:00'),
(14,2,  7,  'Co-Captain', '2025-09-25 10:00'),
(15,3,  8,  'Captain',    '2025-09-25 10:10'),
(16,4,  8,  'Co-Captain', '2025-09-25 10:10'),
(17,5,  9,  'Captain',    '2025-09-25 10:20'),
(18,6,  9,  'Co-Captain', '2025-09-25 10:20'),
(19,7, 10,  'Captain',    '2025-09-25 10:30'),
(20,8, 10,  'Co-Captain', '2025-09-25 10:30'),
(21,9, 11,  'Captain',    '2025-09-25 10:40'),
(22,10,11,  'Co-Captain', '2025-09-25 10:40'),
(23,11,12,  'Captain',    '2025-09-25 10:50'),
(24,12,12,  'Co-Captain', '2025-09-25 10:50');

                     
-- BOOKING (15 rows) 
INSERT INTO Booking (bookingID, flightID, firstName, lastName, email, seatNo, status, lastUpdate) VALUES
(1,  1, 'Liam',   'de Boer', 'liam@example.com',  '12A', 'Booked',      '2025-09-25 12:00'),
(2,  1, 'Eva',    'Khan',    'eva@example.com',   '12B', 'Checked-in',  '2025-09-25 12:05'),
(3,  2, 'Noah',   'Smith',   'noah@example.com',  '14C', 'Booked',      '2025-09-25 12:10'),
(4,  2, 'Mila',   'Verde',   'mila@example.com',  NULL,  'Booked',      '2025-09-25 12:12'),
(5,  3, 'Arthur', 'Nguyen',  'arthur@example.com','2A',  'Booked',      '2025-09-25 12:15'),
(6,  3, 'Sofia',  'Rossi',   'sofia@example.com', '2B',  'Cancelled',   '2025-09-25 12:18'),
(7,  4, 'Ben',    'Lewis',   'ben@example.com',   '6D',  'Booked',      '2025-09-25 12:20'),
(8,  5, 'Aya',    'Tanaka',  'aya@example.com',   '22F', 'Booked',      '2025-09-25 12:25'),
(9,  5, 'Leo',    'Costa',   'leo@example.com',   '22E', 'Booked',      '2025-09-25 12:26'),
(10, 6, 'Ivy',    'Hsu',     'ivy@example.com',   '8A',  'Checked-in',  '2025-09-25 12:30'),
(11, 7, 'Marta',  'Ruiz',    'marta@example.com', '9C',  'Booked',      '2025-09-25 12:35'),
(12, 8, 'Yara',   'Haddad',  'yara@example.com',  NULL,  'Booked',      '2025-09-25 12:37'),
(13, 9, 'Owen',   'Kim',     'owen@example.com',  '15A', 'Booked',      '2025-09-25 12:40'),
(14,10, 'Sara',   'Bauer',   'sara@example.com',  '4B',  'Booked',      '2025-09-25 12:45'),
(15,12, 'Timo',   'Koenig',  'timo@example.com',  '17C', 'Booked',      '2025-09-25 12:50');
       
COMMIT;
""")

# Save changes
conn.commit()
conn.close()
print("Sample data inserted successfully!")
