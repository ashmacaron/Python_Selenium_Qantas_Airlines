# test_qantas_oneway_flight_booking.py
import pytest
import logging
from pageObject.page_objects import FlightBookingPage

# Set up logger for this test module
logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.oneway
class TestQantasOneWayFlightBookingValidation:
    """
    Test Suite: Qantas One-Way Flight Booking Validation
    Test Case ID: TC_QANTAS_ONEWAY_001
    """

    def testcase1_successful_oneway_flight(self, set_up, test_data):
        """
        Test Case: Verify that a user can successfully book a one-way flight

        Test ID: TC_QANTAS_ONEWAY_001
        Test Objective: Verify that a user can successfully book a one-way flight.
        Precondition: User is on QANTAS Airlines homepage

        Test Steps:
        1. Select one-way flight option
        2. Enter origin: Hong Kong
        3. Enter destination: Tokyo
        4. Select departure date: 15 Sept 2025
        5. Confirm passenger selection (1 Adult default)
        6. Click Search Flights
        7. Validate navigation to flight selection page
        """
        logger.info("=" * 80)
        logger.info("Starting Test: TC_QANTAS_ONEWAY_001")
        logger.info("Test Objective: Verify that a user can successfully book a one-way flight")
        logger.info("=" * 80)

        page = set_up
        flight_page = FlightBookingPage(page)

        try:
            # Step 1: Select one-way flight (default might already be selected)
            logger.info("Step 1: Selecting one-way flight option")
            flight_page.select_one_way()
            logger.info("✓ One-way flight option selected")

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

            # Step 5: Select Departure Date - 15 Sept 2025
            departure_date = test_data["dates"]["departure"]
            logger.info(f"Step 5: Selecting departure date: {departure_date}")
            flight_page.select_departure_date(departure_date)
            logger.info(f"✓ Departure date selected: {departure_date}")

            # Step 6: Click on "Search Flights"
            logger.info("Step 6: Initiating flight search")
            flight_page.confirm_search_flights()
            logger.info("✓ Search Flights button clicked")

            # Step 7: Validate User is navigated to select flight page
            logger.info("Step 7: Validating navigation to flight selection page")
            page.wait_for_timeout(5000)  # Wait for page to load

            is_on_flight_page = flight_page.is_on_flight_selection_page()
            logger.info(f"Flight selection page status: {is_on_flight_page}")

            assert is_on_flight_page, "User should be on flight selection page"
            logger.info("✓ Successfully navigated to flight selection page")

            logger.info("=" * 80)
            logger.info(" TEST PASSED: One-way flight booking completed successfully")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f" TEST FAILED: {str(e)}")
            logger.error("Taking screenshot for debugging...")
            flight_page.take_screenshot("oneway_flight_booking_error")
            raise