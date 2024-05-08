from datetime import datetime
import sqlite3

class TripLegType:
    ACCOMMODATION = 1
    POINT_OF_INTEREST = 2
    TRANSFER_POINT = 3

class UserType:
    TRIP_COORDINATOR = 1
    TRIP_MANAGER = 2
    ADMINISTRATOR = 3

class Trip:
    def __init__(self, name, start_date, duration, contact_info):
        self.name = name
        self.start_date = start_date
        self.duration = duration
        self.contact_info = contact_info
        self.trip_legs = []

    def add_trip_leg(self, trip_leg):
        self.trip_legs.append(trip_leg)

class TripLeg:
    def __init__(self, start_location, destination, transport_provider, mode_of_transport, leg_type, cost):
        self.start_location = start_location
        self.destination = destination
        self.transport_provider = transport_provider
        self.mode_of_transport = mode_of_transport
        self.leg_type = leg_type
        self.cost = cost

class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

class Traveller:
    def __init__(self, name, address, date_of_birth, emergency_contact, government_id):
        self.name = name
        self.address = address
        self.date_of_birth = date_of_birth
        self.emergency_contact = emergency_contact
        self.government_id = government_id

class TripCoordinator(User):
    def __init__(self, username):
        super().__init__(username, UserType.TRIP_COORDINATOR)
        self.passengers = []

    def manage_passengers(self, passengers):
        self.passengers = passengers

    def generate_itinerary(self, trip):
        itinerary = f"Trip Name: {trip.name}\nStart Date: {trip.start_date}\nDuration: {trip.duration} days\n"
        for i, trip_leg in enumerate(trip.trip_legs, start=1):
            itinerary += f"\nLeg {i}:\nStart Location: {trip_leg.start_location}\nDestination: {trip_leg.destination}\n"
            itinerary += f"Transport Provider: {trip_leg.transport_provider}\nMode of Transport: {trip_leg.mode_of_transport}\n"
            itinerary += f"Leg Type: {trip_leg.leg_type}\nCost: ${trip_leg.cost}\n"
        return itinerary

class TripManager(TripCoordinator):
    def __init__(self, username):
        super().__init__(username)
        self.trip_coordinators = []

    def add_trip_coordinator(self, trip_coordinator):
        self.trip_coordinators.append(trip_coordinator)

    def generate_invoice(self, trip):
        total_cost = sum(trip_leg.cost for trip_leg in trip.trip_legs)
        return f"Invoice for {trip.name}:\nTotal Cost: ${total_cost}"

class Administrator(TripManager):
    def __init__(self, username):
        super().__init__(username)
        self.trip_managers = []

    def add_trip_manager(self, trip_manager):
        self.trip_managers.append(trip_manager)

    def view_invoices(self, trips):
        invoice_totals = {}
        for trip in trips:
            total_cost = sum(trip_leg.cost for trip_leg in trip.trip_legs)
            invoice_totals[trip.name] = total_cost
        return invoice_totals

    def delete_invoice(self, trip_name, trips):
        for trip in trips:
            if trip.name == trip_name:
                trips.remove(trip)
                return
        print(f"Invoice for trip '{trip_name}' not found.")

class TravellerManager:
    def __init__(self):
        self.travellers = []

    def add_traveller(self, traveller):
        self.travellers.append(traveller)

    def view_travellers(self):
        for traveller in self.travellers:
            print(f"Name: {traveller.name}, Address: {traveller.address}, Date of Birth: {traveller.date_of_birth}, Emergency Contact: {traveller.emergency_contact}, Government ID: {traveller.government_id}")

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor

    def close_connection(self):
        self.conn.close()

def create_trip():
    name = input("Enter trip name: ")
    start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), '%Y-%m-%d')
    duration = int(input("Enter duration in days: "))
    contact_info = input("Enter contact information: ")
    return Trip(name, start_date, duration, contact_info)

def view_trips(trips):
    for trip in trips:
        print(f"Name: {trip.name}, Start Date: {trip.start_date}, Duration: {trip.duration}, Contact Info: {trip.contact_info}")

def update_trip(trips):
    trip_name = input("Enter the name of the trip to update: ")
    for trip in trips:
        if trip.name == trip_name:
            trip.name = input("Enter new name: ")
            trip.start_date = datetime.strptime(input("Enter new start date (YYYY-MM-DD): "), '%Y-%m-%d')
            trip.duration = int(input("Enter new duration in days: "))
            trip.contact_info = input("Enter new contact information: ")
            print("Trip updated successfully.")
            return
    print("Trip not found.")

def delete_trip(trips):
    trip_name = input("Enter the name of the trip to delete: ")
    for trip in trips:
        if trip.name == trip_name:
            trips.remove(trip)
            print("Trip deleted successfully.")
            return
    print("Trip not found.")

def create_traveller():
    return Traveller(input("Enter name: "), input("Enter address: "), datetime.strptime(input("Enter DOB (YYYY-MM-DD): "), '%Y-%m-%d'), input("Enter emergency contact: "), input("Enter government ID: "))

def add_trip_leg(trip):
    start_location = input("Enter start location: ")
    destination = input("Enter destination: ")
    transport_provider = input("Enter transport provider: ")
    mode_of_transport = input("Enter mode of transport: ")
    leg_type = input("Enter leg type (1: Accommodation, 2: Point of Interest, 3: Transfer Point): ")
    cost = float(input("Enter cost: "))
    trip_leg = TripLeg(start_location, destination, transport_provider, mode_of_transport, leg_type, cost)
    trip.add_trip_leg(trip_leg)
    print("Trip leg added successfully.")

def view_trip_legs(trip):
    for i, trip_leg in enumerate(trip.trip_legs, start=1):
        print(f"Leg {i}: Start Location: {trip_leg.start_location}, Destination: {trip_leg.destination}, Transport Provider: {trip_leg.transport_provider}, Mode of Transport: {trip_leg.mode_of_transport}, Leg Type: {trip_leg.leg_type}, Cost: {trip_leg.cost}")

def update_trip_leg(trip):
    leg_index = int(input("Enter the index of the leg to update: ")) - 1
    if 0 <= leg_index < len(trip.trip_legs):
        trip_leg = trip.trip_legs[leg_index]
        trip_leg.start_location = input("Enter new start location: ")
        trip_leg.destination = input("Enter new destination: ")
        trip_leg.transport_provider = input("Enter new transport provider: ")
        trip_leg.mode_of_transport = input("Enter new mode of transport: ")
        trip_leg.leg_type = input("Enter new leg type (1: Accommodation, 2: Point of Interest, 3: Transfer Point): ")
        trip_leg.cost = float(input("Enter new cost: "))
        print("Trip leg updated successfully.")
    else:
        print("Invalid leg index.")

def delete_trip_leg(trip):
    leg_index = int(input("Enter the index of the leg to delete: ")) - 1
    if 0 <= leg_index < len(trip.trip_legs):
        trip.trip_legs.pop(leg_index)
        print("Trip leg deleted successfully.")
    else:
        print("Invalid leg index.")

def manage_passengers(trip, passengers):
    trip_coordinator = TripCoordinator(input("Enter trip coordinator username: "))
    trip_coordinator.manage_passengers(passengers)
    print("Passengers managed successfully.")

def update_trip_legs(trip):
    leg_index = int(input("Enter the index of the leg to update: ")) - 1
    if 0 <= leg_index < len(trip.trip_legs):
        trip_leg = trip.trip_legs[leg_index]
        trip_leg.start_location = input("Enter new start location: ")
        trip_leg.destination = input("Enter new destination: ")
        trip_leg.transport_provider = input("Enter new transport provider: ")
        trip_leg.mode_of_transport = input("Enter new mode of transport: ")
        trip_leg.leg_type = input("Enter new leg type (1: Accommodation, 2: Point of Interest, 3: Transfer Point): ")
        trip_leg.cost = float(input("Enter new cost: "))
        print("Trip leg updated successfully.")
    else:
        print("Invalid leg index.")

def generate_itinerary(trip):
    trip_coordinator = TripCoordinator(input("Enter trip coordinator username: "))
    print(trip_coordinator.generate_itinerary(trip))

def handle_payments(trip):
    trip_manager = TripManager(input("Enter trip manager username: "))
    print(trip_manager.generate_invoice(trip))

def perform_trip_coordinator_tasks(trip):
    trip_coordinator = TripCoordinator(input("Enter trip coordinator username: "))
    trip_coordinator.manage_passengers([])
    print(trip_coordinator.generate_itinerary(trip))

def create_delete_trip_coordinators():
    trip_manager = TripManager(input("Enter trip manager username: "))
    trip_manager.add_trip_coordinator(TripCoordinator(input("Enter trip coordinator username to add: ")))
    print("Trip coordinator added successfully.")

def generate_total_invoices():
    administrator = Administrator(input("Enter administrator username: "))
    trips = []  # Populate trips list with actual trip objects
    print(administrator.view_invoices(trips))

def perform_trip_manager_tasks(trip):
    trip_manager = TripManager(input("Enter trip manager username: "))
    print(trip_manager.generate_invoice(trip))

def create_delete_trip_managers():
    administrator = Administrator(input("Enter administrator username: "))
    trip_manager = TripManager(input("Enter trip manager username to add: "))
    administrator.add_trip_manager(trip_manager)
    print("Trip manager added successfully.")

def view_delete_trip_invoices(trips):
    administrator = Administrator(input("Enter administrator username: "))
    trip_name = input("Enter trip name to delete invoice: ")
    administrator.delete_invoice(trip_name, trips)

def view_delete_trip_payments(trips):
    administrator = Administrator(input("Enter administrator username: "))
    trip_name = input("Enter trip name to delete payment: ")
    administrator.delete_invoice(trip_name, trips)

def main():
    db_manager = DatabaseManager("travel_management.db")

    db_manager.execute_query("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY,
            name TEXT,
            start_date TEXT,
            duration INTEGER,
            contact_info TEXT
        )
    """)

    db_manager.execute_query("""
        CREATE TABLE IF NOT EXISTS trip_legs (
            id INTEGER PRIMARY KEY,
            trip_id INTEGER,
            start_location TEXT,
            destination TEXT,
            transport_provider TEXT,
            mode_of_transport TEXT,
            leg_type INTEGER,
            cost REAL,
            FOREIGN KEY(trip_id) REFERENCES trips(id)
        )
    """)

    trips = []
    travellers = TravellerManager()

    while True:
        print("1. Create Trip")
        print("2. View Trips")
        print("3. Update Trip")
        print("4. Delete Trip")
        print("5. Create Traveller")
        print("6. View Travellers")
        print("7. Add Trip Leg")
        print("8. View Trip Legs")
        print("9. Update Trip Leg")
        print("10. Delete Trip Leg")
        print("11. Manage Passengers")
        print("12. Update Trip Legs")
        print("13. Generate Itinerary")
        print("14. Handle Payments")
        print("15. Perform Trip Coordinator Tasks")
        print("16. Create/Delete Trip Coordinators")
        print("17. Generate Total Invoices")
        print("18. Perform Trip Manager Tasks")
        print("19. Create/Delete Trip Managers")
        print("20. View/Delete Trip Invoices")
        print("21. View/Delete Trip Payments")
        print("22. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            trip = create_trip()
            trips.append(trip)
        elif choice == '2':
            view_trips(trips)
        elif choice == '3':
            update_trip(trips)
        elif choice == '4':
            delete_trip(trips)
        elif choice == '5':
            traveller = create_traveller()
            travellers.add_traveller(traveller)
        elif choice == '6':
            travellers.view_travellers()
        elif choice == '7':
            add_trip_leg(trip)
        elif choice == '8':
            view_trip_legs(trip)
        elif choice == '9':
            update_trip_leg(trip)
        elif choice == '10':
            delete_trip_leg(trip)
        elif choice == '11':
            manage_passengers(trip, [])
        elif choice == '12':
            update_trip_legs(trip)
        elif choice == '13':
            generate_itinerary(trip)
        elif choice == '14':
            handle_payments(trip)
        elif choice == '15':
            perform_trip_coordinator_tasks(trip)
        elif choice == '16':
            create_delete_trip_coordinators()
        elif choice == '17':
            generate_total_invoices()
        elif choice == '18':
            perform_trip_manager_tasks(trip)
        elif choice == '19':
            create_delete_trip_managers()
        elif choice == '20':
            view_delete_trip_invoices(trips)
        elif choice == '21':
            view_delete_trip_payments(trips)
        elif choice == '22':
            break
        else:
            print("Invalid choice. Please try again.")

    db_manager.close_connection()

if __name__ == "__main__":
    main()
