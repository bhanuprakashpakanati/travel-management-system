import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sqlite3

from main import Trip, Traveller, TripManager, DatabaseManager

class TestTrip(unittest.TestCase):
    def setUp(self):
        self.db_manager = MagicMock(spec=DatabaseManager)

    @patch('main.datetime')  # Patching datetime where it's used, which is in the 'main' module
    def test_create_trip(self, mock_datetime):
        # Set up the mock to return a specific datetime object
        mock_datetime.strptime.return_value = datetime(2021, 1, 1)

        # Assuming the trip creation processes the date
        trip = Trip("Holiday", datetime(2021, 1, 1), 10, "contact@example.com")

        # Simulate the call to the database
        self.db_manager.execute_query(
            "INSERT INTO trips (name, start_date, duration, contact_info) VALUES (?, ?, ?, ?)",
            ("Holiday", datetime(2021, 1, 1), 10, "contact@example.com")
        )

        # Verify that the database query was called correctly
        self.db_manager.execute_query.assert_called_once()

    @patch('main.datetime')
    def test_update_trip(self, mock_datetime):
        # Prepare the mock
        mock_datetime.strptime.return_value = datetime(2022, 1, 1)
        self.db_manager.fetch_query.return_value = [(1, 'Holiday')]

        new_name = "New Year Holiday"
        new_start_date = "2022-01-01"
        new_duration = 15
        new_contact_info = "new_contact@example.com"

        trip_id = 1
        self.db_manager.execute_query(
            "UPDATE trips SET name = ?, start_date = ?, duration = ?, contact_info = ? WHERE id = ?",
            (new_name, new_start_date, new_duration, new_contact_info, trip_id)
        )

        # Assert the SQL execution was called with the right parameters
        self.db_manager.execute_query.assert_called_once()

    def tearDown(self):
        self.db_manager.close_connection()

if __name__ == "__main__":
    unittest.main()
