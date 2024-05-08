from datetime import datetime
import sqlite3
from enum import Enum
import json
import os
from pprint import pprint
import random
import tkinter as tk
from tkinter import ttk
from typing import List, Dict
import unittest

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
        self.user_type = UserType.TRIP_MANAGER
        self.trip_coordinators = []

    def add_trip_coordinator(self, trip_coordinator):
        self.trip_coordinators.append(trip_coordinator)

    def generate_invoice(self, trip):
        total_cost = sum(trip_leg.cost for trip_leg in trip.trip_legs)
        return f"Invoice for {trip.name}:\nTotal Cost: ${total_cost}"

class Administrator(TripManager):
    def __init__(self, username):
        super().__init__(username)
        self.user_type = UserType.ADMINISTRATOR
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
                print(f"Invoice for trip '{trip_name}' deleted successfully.")
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

    def fetch_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

def create_trip(db_manager):
    name = input("Enter trip name: ")
    try:
        start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please try again.")
        return None
    duration = int(input("Enter duration in days: "))
    contact_info = input("Enter contact information: ")
    trip = Trip(name, start_date, duration, contact_info)
    db_manager.execute_query(
        "INSERT INTO trips (name, start_date, duration, contact_info) VALUES (?, ?, ?, ?)",
        (name, start_date, duration, contact_info)
    )
    print(f"Trip created successfully: {trip.name}")
    return trip

def view_trips(db_manager):
    trips = db_manager.fetch_query("SELECT name, start_date, duration, contact_info FROM trips")
    if not trips:
        print("No trips available to display.")
    else:
        for trip in trips:
            print(f"Name: {trip[0]}, Start Date: {trip[1]}, Duration: {trip[2]} days, Contact Info: {trip[3]}")
        input("Press any key to continue...")  # This will pause the script until a key is pressed


def update_trip(db_manager):
    trip_name = input("Enter the name of the trip to update: ")
    trip = db_manager.fetch_query("SELECT id, name FROM trips WHERE name = ?", (trip_name,))
    if trip:
        trip_id = trip[0][0]
        new_name = input("Enter new name: ")
        new_start_date = input("Enter new start date (YYYY-MM-DD): ")
        new_duration = input("Enter new duration in days: ")
        new_contact_info = input("Enter new contact information: ")

        try:
            datetime.strptime(new_start_date, '%Y-%m-%d')  # Validate date format
            db_manager.execute_query("""
                UPDATE trips SET name = ?, start_date = ?, duration = ?, contact_info = ?
                WHERE id = ?
            """, (new_name, new_start_date, new_duration, new_contact_info, trip_id))
            print("Trip updated successfully.")
        except ValueError:
            print("Invalid date format. Please try again.")
    else:
        print("Trip not found.")


def delete_trip(db_manager):
    trip_name = input("Enter the name of the trip to delete: ")
    trip = db_manager.fetch_query("SELECT id FROM trips WHERE name = ?", (trip_name,))
    if trip:
        trip_id = trip[0][0]
        db_manager.execute_query("DELETE FROM trips WHERE id = ?", (trip_id,))
        db_manager.execute_query("DELETE FROM trip_legs WHERE trip_id = ?", (trip_id,))  # Also delete related trip legs
        print("Trip deleted successfully.")
    else:
        print("Trip not found.")



def create_traveller(db_manager):
    name = input("Enter the traveler's name: ")
    address = input("Enter the traveler's address: ")
    date_of_birth = input("Enter the traveler's date of birth (YYYY-MM-DD): ")
    emergency_contact = input("Enter the emergency contact: ")
    government_id = input("Enter the government ID number: ")

    try:
        datetime.strptime(date_of_birth, '%Y-%m-%d')  # Validate date format
        db_manager.execute_query(
            "INSERT INTO travellers (name, address, date_of_birth, emergency_contact, government_id) VALUES (?, ?, ?, ?, ?)",
            (name, address, date_of_birth, emergency_contact, government_id)
        )
        print(f"Traveler {name} created successfully.")
    except ValueError:
        print("Invalid date format. Please try again.")

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

    db_manager.execute_query("""
        CREATE TABLE IF NOT EXISTS travellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            date_of_birth DATE,
            emergency_contact TEXT,
            government_id TEXT
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
        print("11. Handle Payments")
        print("12. Create/Delete Trip Coordinators")
        print("13. Generate Total Invoices")
        print("14. Create/Delete Trip Managers")
        print("15. View/Delete Trip Invoices")
        print("16. View/Delete Trip Payments")
        print("17. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_trip(db_manager)
        elif choice == '2':
            view_trips(db_manager)
        elif choice == '3':
            update_trip(db_manager)
        elif choice == '4':
            delete_trip(db_manager)
        elif choice == '5':
            pass
        elif choice == '6':
            pass
        elif choice == '7':
            pass
        elif choice == '8':
            pass
        elif choice == '9':
            pass
        elif choice == '10':
            pass
        elif choice == '11':
            pass
        elif choice == '12':
            pass
        elif choice == '13':
            pass
        elif choice == '14':
            pass
        elif choice == '15':
            pass
        elif choice == '16':
            pass
        elif choice == '17':
            break
        else:
            print("Invalid choice. Please try again.")

    db_manager.close_connection()

if __name__ == "__main__":
    main()
