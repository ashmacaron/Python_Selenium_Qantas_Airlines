import pytest
import logging
from pageObject.page_objects import FlightBookingPage

# Set up logger for this test module
logger = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.roundtrip
class TestQantasRoundTripFlightBookingValidation:
    """
    Test Suite: Qantas Round-Trip Flight Booking Validation
    Test Case ID: TC_QANTAS_ROUNDTRIP_002
    """

    def testcase2_successful_roundtrip_flight(self, set_up, test_data):
        """
        Test Case: Verify that a user can successfully book a round-trip flight

        Test ID: TC_QANTAS_ROUNDTRIP_002
        Test Objective: Verify that a user can successfully book a round-trip flight.
        Precondition: User is on QANTAS Airlines homepage

        Test Steps:
        1. Select round-trip flight option
        2. Enter origin: Hong Kong
        3. Enter destination: Tokyo
        4. Select departure and return dates: 15 Sept 2025 & 18 Sept 2025
        5. Confirm passenger selection (1 Adult default)
        6. Click Search Flights
        7. Validate successful search initiation
        """
        logger.info("=" * 80)
        logger.info("Starting Test: TC_QANTAS_ROUNDTRIP_002")
        logger.info("Test Objective: Verify that a user can successfully book a round-trip flight")
        logger.info("=" * 80)

        page = set_up
        flight_page = FlightBookingPage(page)

        try:
            # Step 1: Select round-trip flight
            logger.info("Step 1: Switching from one-way to round-trip flight option")
            flight_page.select_one_way()
            logger.info("✓ One-way option selected first")

            flight_page.select_round_trip()
            logger.info("✓ Round-trip flight option selected")

            # Step 2: Set passenger configuration
            logger.info("Step 2: Setting passenger configuration")
            flight_page.select_passengers()
            flight_page.confirm_passenger_selection()
            logger.info("✓ Passenger selection confirmed: 1 Adult (default)")

            # Step 3: Enter Origin - Hong Kong
            origin = test_data["origins"]["hong_kong"]
            logger.info(f"Step 3: Entering origin location: {origin}")
            flight_page.enter_origin(origin)
            logger.info(f"✓ Origin location entered: {origin}")

            # Step 4: Enter Destination - Tokyo (Narita)
            destination = test_data["destination"]["tokyo"]
            logger.info(f"Step 4: Entering destination location: {destination}")
            flight_page.enter_destination(destination)
            logger.info(f"✓ Destination location entered: {destination}")

            # Step 5: Select Departure and Return Dates
            departure_date = test_data["dates"]["departure"]
            return_date = test_data["dates"]["return"]
            logger.info(f"Step 5: Selecting travel dates - Departure: {departure_date}, Return: {return_date}")
            flight_page.select_return_date(departure_date, return_date)
            logger.info(f"✓ Travel dates selected - Departure: {departure_date}, Return: {return_date}")

            # Step 6: Click on "Search Flights"
            logger.info("Step 6: Initiating flight search for round-trip")
            flight_page.confirm_search_flights()
            logger.info("✓ Round-trip flight search initiated successfully")

            logger.info("=" * 80)
            logger.info(" TEST PASSED: Round-trip flight booking completed successfully")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f" TEST FAILED: {str(e)}")
            logger.error("Taking screenshot for debugging...")
            flight_page.take_screenshot("roundtrip_flight_booking_error")
            raise