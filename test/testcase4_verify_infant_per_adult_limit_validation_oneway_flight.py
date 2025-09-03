import pytest
import logging
from pageObject.page_objects import FlightBookingPage

# Set up logger for this test module
logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.validation
@pytest.mark.passenger
class TestQantasOneWayFlightInfantLimitValidation:
    """
    Test Suite: Qantas One-Way Flight Infant Limit Validation
    Test Case ID: TC_QANTAS_INFANT_LIMIT_004
    """

    def testcase4_verify_infant_per_adult_limit_validation_oneway_flight(self, set_up, test_data):
        """
        Test Case: Verify that a user can only have 1 infant per adult

        Test ID: TC_QANTAS_INFANT_LIMIT_004
        Test Objective: Verify that a user can only have 1 infant per adult.
        Precondition: User is on QANTAS Airlines homepage

        Test Steps:
        1. Select one-way flight option
        2. Enter origin: Hong Kong
        3. Enter destination: Tokyo
        4. Select departure date: 15 Sept 2025
        5. Set passenger configuration: 1 Adult (default)
        6. Add 1 infant (valid scenario)
        7. Attempt to add 2nd infant (should trigger validation)
        8. Validate error message for infant limit exceeded
        """
        logger.info("=" * 80)
        logger.info("Starting Test: TC_QANTAS_INFANT_LIMIT_004")
        logger.info("Test Objective: Verify that a user can only have 1 infant per adult")
        logger.info("=" * 80)

        page = set_up
        flight_page = FlightBookingPage(page)

        try:
            # Step 1: Select one-way flight
            logger.info("Step 1: Selecting one-way flight option")
            flight_page.select_one_way()
            logger.info("✓ One-way flight option selected")

            # Step 2: Enter Origin - Hong Kong
            origin = test_data["origins"]["hong_kong"]
            logger.info(f"Step 2: Entering origin location: {origin}")
            flight_page.enter_origin(origin)
            logger.info(f"✓ Origin location entered: {origin}")

            # Step 3: Enter Destination - Tokyo (Narita)
            destination = test_data["destination"]["tokyo"]
            logger.info(f"Step 3: Entering destination location: {destination}")
            flight_page.enter_destination(destination)
            logger.info(f"✓ Destination location entered: {destination}")

            # Step 4: Select Departure Date
            departure_date = test_data["dates"]["departure"]
            logger.info(f"Step 4: Selecting departure date: {departure_date}")
            flight_page.select_departure_date(departure_date)
            logger.info(f"✓ Departure date selected: {departure_date}")

            # Step 5: Select 1 adult passenger (Default)
            adults = test_data["passengers"]["adult"]
            logger.info(f"Step 5: Setting adult passenger count: {adults}")
            flight_page.select_passengers(adults=adults)
            logger.info(f"✓ Adult passenger count set: {adults}")

            # Step 6: Add 1 infant (valid scenario)
            logger.info("Step 6: Adding 1st infant (valid - within limit)")
            first_infant_added = flight_page.click_infant_plus()
            if first_infant_added:
                logger.info("✓ First infant added successfully")
                current_infant_count = flight_page.get_infant_count()
                logger.info(f"Current infant count: {current_infant_count}")
            else:
                logger.warning("⚠ First infant could not be added")

            # Step 7: Try to add 2nd infant (should trigger validation)
            logger.info("Step 7: Attempting to add 2nd infant (should exceed limit)")
            second_infant_added = flight_page.click_infant_plus()
            if second_infant_added:
                logger.warning("⚠ Second infant was added (unexpected)")
            else:
                logger.info("✓ Second infant blocked (expected behavior)")

            # Wait for UI to update and validation to trigger
            page.wait_for_timeout(1000)

            # Step 8: Validate infant limit error message
            logger.info("Step 8: Validating infant limit error message")

            error_message = flight_page.get_error_message()
            expected_error = test_data["expected_messages"]["infant_limit_error"]

            logger.info(f"Captured error message: '{error_message}'")
            logger.info(f"Expected error pattern: '{expected_error}'")

            # Check if infant plus button is disabled as additional validation
            is_infant_plus_disabled = flight_page.is_infant_plus_disabled()
            logger.info(f"Infant plus button disabled status: {is_infant_plus_disabled}")

            # Primary validation - error message
            assert error_message is not None, "Error message should be displayed for infant limit exceeded"
            logger.info("✓ Error message is present")

            assert expected_error.lower() in error_message.lower(), \
                f"Expected error message '{expected_error}' not found in '{error_message}'"
            logger.info("✓ Infant limit error message validated successfully")

            # Secondary validation - button state (if applicable)
            if is_infant_plus_disabled:
                logger.info("✓ Infant plus button is disabled (additional validation)")

            logger.info("=" * 80)
            logger.info(" TEST PASSED: Infant per adult limit validation working correctly")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f" TEST FAILED: {str(e)}")
            logger.error("Taking screenshot for debugging...")
            flight_page.take_screenshot("infant_limit_validation_error")
            raise