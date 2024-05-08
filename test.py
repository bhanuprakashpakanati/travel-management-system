import unittest
from datetime import datetime
from unittest.mock import patch

class TestTravelManagementSystem(unittest.TestCase):

    def setUp(self):
        self.trip = Trip("Test Trip", datetime(2023, 6, 1), 7, "test@example.com")
        self.trip_leg = TripLeg("New York", "Los Angeles", "ABC Airlines", "Flight", TripLegType.TRANSFER_POINT, 500.0)
        self.traveller = Traveller("John Doe", "123 Main St", datetime(1990, 1, 1), "555-1234", "123456789")

    def test_trip_creation(self):
        self.assertEqual(self.trip.name, "Test Trip")
        self.assertEqual(self.trip.start_date, datetime(2023, 6, 1))
        self.assertEqual(self.trip.duration, 7)
        self.assertEqual(self.trip.contact_info, "test@example.com")
        self.assertEqual(len(self.trip.trip_legs), 0)

    def test_add_trip_leg(self):
        self.trip.add_trip_leg(self.trip_leg)
        self.assertEqual(len(self.trip.trip_legs), 1)
        self.assertIn(self.trip_leg, self.trip.trip_legs)

    def test_trip_leg_creation(self):
        self.assertEqual(self.trip_leg.start_location, "New York")
        self.assertEqual(self.trip_leg.destination, "Los Angeles")
        self.assertEqual(self.trip_leg.transport_provider, "ABC Airlines")
        self.assertEqual(self.trip_leg.mode_of_transport, "Flight")
        self.assertEqual(self.trip_leg.leg_type, TripLegType.TRANSFER_POINT)
        self.assertEqual(self.trip_leg.cost, 500.0)

    def test_traveller_creation(self):
        self.assertEqual(self.traveller.name, "John Doe")
        self.assertEqual(self.traveller.address, "123 Main St")
        self.assertEqual(self.traveller.date_of_birth, datetime(1990, 1, 1))
        self.assertEqual(self.traveller.emergency_contact, "555-1234")
        self.assertEqual(self.traveller.government_id, "123456789")

    @patch('builtins.input', side_effect=['Test Coordinator'])
    def test_trip_coordinator_generate_itinerary(self, mock_input):
        trip_coordinator = TripCoordinator("Test Coordinator")
        self.trip.add_trip_leg(self.trip_leg)
        itinerary = trip_coordinator.generate_itinerary(self.trip)
        expected_itinerary = f"Trip Name: {self.trip.name}\nStart Date: {self.trip.start_date}\nDuration: {self.trip.duration} days\n\nLeg 1:\nStart Location: {self.trip_leg.start_location}\nDestination: {self.trip_leg.destination}\nTransport Provider: {self.trip_leg.transport_provider}\nMode of Transport: {self.trip_leg.mode_of_transport}\nLeg Type: {self.trip_leg.leg_type}\nCost: ${self.trip_leg.cost}\n"
        self.assertEqual(itinerary, expected_itinerary)

    @patch('builtins.input', side_effect=['Test Manager'])
    def test_trip_manager_generate_invoice(self, mock_input):
        trip_manager = TripManager("Test Manager")
        self.trip.add_trip_leg(self.trip_leg)
        invoice = trip_manager.generate_invoice(self.trip)
        expected_invoice = f"Invoice for {self.trip.name}:\nTotal Cost: ${self.trip_leg.cost}"
        self.assertEqual(invoice, expected_invoice)

    def test_traveller_manager(self):
        traveller_manager = TravellerManager()
        traveller_manager.add_traveller(self.traveller)
        self.assertEqual(len(traveller_manager.travellers), 1)
        self.assertIn(self.traveller, traveller_manager.travellers)

if __name__ == '__main__':
    unittest.main()
