import pytest
import logging
from pageObject.page_objects import FlightBookingPage

# Set up logger for this test module
logger = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.validation
class TestQantasRoundTripMissingReturnDateValidation:
    """
    Test Suite: Qantas Round-Trip Flight Missing Return Date Validation
    Test Case ID: TC_QANTAS_ROUNDTRIP_NEGATIVE_003
    """

    def testcase3_roundtrip_with_missing_return_date(self, set_up, test_data):
        """
        Test Case: Verify that a user cannot proceed without selecting a Return Date in Round-Trip Flight

        Test ID: TC_QANTAS_ROUNDTRIP_NEGATIVE_003
        Test Objective: Verify that a user cannot proceed without selecting a Return Date in Round-Trip Flight
        Precondition: User is on QANTAS Airlines homepage

        Test Steps:
        1. Select round-trip flight option
        2. Enter origin: Hong Kong
        3. Enter destination: Tokyo
        4. Select only departure date: 15 Sept 2025
        5. Leave return date blank
        6. Close date picker
        7. Click Search Flights
        8. Validate error message appears for missing return date
        """
        logger.info("=" * 80)
        logger.info("Starting Test: TC_QANTAS_ROUNDTRIP_NEGATIVE_003")
        logger.info(
            "Test Objective: Verify that a user cannot proceed without selecting a Return Date in Round-Trip Flight")
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

            # Step 5: Select Departure Date Only (Leave Return Date Blank)
            departure_date = test_data["dates"]["departure"]
            logger.info(f"Step 5: Selecting only departure date: {departure_date}")
            flight_page.select_departure_date(departure_date)
            logger.info(f"✓ Departure date selected: {departure_date}")
            logger.info("⚠ Return date intentionally left blank for validation test")

            # Step 6: Close the Date Picker after selecting departure date
            logger.info("Step 6: Closing date picker without selecting return date")
            flight_page.close_date_picker()
            logger.info("✓ Date picker closed")

            # Step 7: Attempt to Click on "Search Flights"
            logger.info("Step 7: Attempting to search flights without return date")
            flight_page.click_search_flights()
            logger.info("✓ Search Flights button clicked")

            # Step 8: Validate Error Message for Missing Return Date
            logger.info("Step 8: Validating error message for missing return date")
            page.wait_for_timeout(2000)  # Wait for error message to appear

            error_message = flight_page.get_error_message()
            expected_error = test_data["expected_messages"]["return_date_error"]

            logger.info(f"Captured error message: '{error_message}'")
            logger.info(f"Expected error message: '{expected_error}'")

            assert error_message is not None, "Error message should be displayed for missing return date"
            logger.info("✓ Error message is present")

            assert expected_error.lower() in error_message.lower(), \
                f"Expected error message '{expected_error}' not found in '{error_message}'"
            logger.info("✓ Error message content validated successfully")

            logger.info("=" * 80)
            logger.info(" TEST PASSED: Return date validation working correctly")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f" TEST FAILED: {str(e)}")
            logger.error("Taking screenshot for debugging...")
            flight_page.take_screenshot("roundtrip_missing_return_date_error")
            raise