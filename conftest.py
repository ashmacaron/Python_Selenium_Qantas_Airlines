import logging
import pytest
from playwright.sync_api import Playwright
import json
from datetime import datetime
import os
import shutil

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configure logging for the entire test session"""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Generate timestamped log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/test_execution_{timestamp}.log"

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler()  # Also output to console
        ]
    )

    # Set specific logger levels
    logging.getLogger('playwright').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    # Log session start
    session_logger = logging.getLogger("test_session")
    session_logger.info("=" * 80)
    session_logger.info(f"TEST SESSION STARTED - Log file: {log_file}")
    session_logger.info("=" * 80)

    yield log_file

    # Log session end
    session_logger.info("=" * 80)
    session_logger.info("TEST SESSION COMPLETED")
    session_logger.info("=" * 80)


def pytest_configure(config):
    """Configure pytest markers and HTML report"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")

    # Configure HTML report automatically
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)

    html_report = f"{report_dir}/report_{timestamp}.html"
    config.option.htmlpath = html_report

    # Set HTML report title and description
    if not hasattr(config.option, 'html_title'):
        config.option.html_title = "Flight Booking Test Report"

    logger.info(f"HTML report will be generated at: {html_report}")


def pytest_sessionfinish(session, exitstatus):
    """Actions to perform after test session finishes"""
    logger.info("Test session finished, preparing final report...")

    # Create a latest report link for easy access
    if hasattr(session.config.option, 'htmlpath') and session.config.option.htmlpath:
        report_path = session.config.option.htmlpath
        if os.path.exists(report_path):
            # Create a symlink or copy to 'latest_report.html' for easy access
            latest_report = "reports/latest_report.html"
            try:
                if os.path.exists(latest_report):
                    os.remove(latest_report)
                shutil.copy2(report_path, latest_report)
                logger.info(f"Report copied to: {latest_report}")
                logger.info(f"Main report available at: {report_path}")
            except Exception as e:
                logger.error(f"Failed to create latest report copy: {e}")


@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON file"""
    try:
        with open("test_data.json", "r") as f:
            data = json.load(f)
            logger.info("Test data loaded successfully from test_data.json")
            return data
    except FileNotFoundError:
        logger.warning("test_data.json not found, returning empty dict")
        return {}
    except Exception as e:
        logger.error(f"Error loading test data: {e}")
        return {}


@pytest.fixture(scope="function")
def set_up(playwright: Playwright, request):
    """Setup browser and page for each test"""
    test_logger = logging.getLogger(f"setup.{request.node.name}")
    test_logger.info(f"Setting up browser for test: {request.node.name}")

    browser = playwright.chromium.launch(
        slow_mo=1000,
        headless=False,
        args=['--start-maximized']
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    test_logger.info("Navigating to Qantas flight booking page...")
    page.goto("https://www.qantas.com/hk/en/book-a-trip/flights.html#make-a-flight-booking")
    page.set_default_timeout(30000)

    test_logger.info("Browser setup completed successfully")

    yield page

    test_logger.info(f"Cleaning up browser for test: {request.node.name}")
    context.close()
    browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Enhanced reporting with screenshots for pytest-html"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # Only process during the 'call' phase (actual test execution)
    if rep.when == "call":
        try:
            # Check if pytest-html is available
            try:
                import pytest_html.extras as extras
            except ImportError:
                logger.warning("pytest-html not installed. Install with: pip install pytest-html")
                return

            # Initialize extra list if it doesn't exist
            if not hasattr(rep, 'extra'):
                rep.extra = []

            # Get the page object from the test
            page = None

            # Try to get page from fixture
            if hasattr(item, '_request'):
                try:
                    page = item._request.getfixturevalue('set_up')
                except Exception:
                    logger.debug("Could not get page from set_up fixture")

            # Alternative method to get page
            if not page and hasattr(item, 'funcargs') and 'set_up' in item.funcargs:
                page = item.funcargs['set_up']

            if page and hasattr(page, 'screenshot'):
                # Create screenshots directory
                screenshots_dir = "screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)

                # Generate timestamp for unique filenames
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Always take a screenshot at test completion
                final_screenshot = f"{screenshots_dir}/{item.name}_{timestamp}_final.png"
                try:
                    page.screenshot(path=final_screenshot, full_page=True)
                    if os.path.exists(final_screenshot):
                        rep.extra.append(extras.image(final_screenshot, name="Final State"))
                        logger.info(f"Final screenshot captured: {final_screenshot}")
                except Exception as e:
                    logger.error(f"Failed to capture final screenshot: {e}")

                # Take additional failure screenshot if test failed
                if rep.failed:
                    failure_screenshot = f"{screenshots_dir}/{item.name}_{timestamp}_FAILURE.png"
                    try:
                        page.screenshot(path=failure_screenshot, full_page=True)
                        if os.path.exists(failure_screenshot):
                            rep.extra.append(extras.image(failure_screenshot, name="FAILURE DETAIL"))
                            logger.error(f"Failure screenshot captured: {failure_screenshot}")
                    except Exception as e:
                        logger.error(f"Failed to capture failure screenshot: {e}")

                # Add page URL to report
                try:
                    current_url = page.url
                    rep.extra.append(extras.text(current_url, name="Page URL"))
                except Exception as e:
                    logger.debug(f"Could not capture URL: {e}")

            else:
                logger.warning(f"No page object available for screenshots in test: {item.name}")

        except Exception as e:
            logger.error(f"Error in pytest_runtest_makereport: {e}")


@pytest.fixture(autouse=True)
def log_test_start_end(request):
    """Log test start and end with results"""
    test_logger = logging.getLogger(f"test.{request.node.name}")

    test_logger.info("*" * 60)
    test_logger.info(f"STARTING TEST: {request.node.name}")
    test_logger.info("*" * 60)

    start_time = datetime.now()

    yield

    end_time = datetime.now()
    duration = end_time - start_time

    # Determine test result
    result_status = "UNKNOWN"
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            result_status = "PASSED"
            test_logger.info(f"✅ TEST PASSED: {request.node.name} (Duration: {duration.total_seconds():.2f}s)")
        elif request.node.rep_call.failed:
            result_status = "FAILED"
            test_logger.error(f"❌ TEST FAILED: {request.node.name} (Duration: {duration.total_seconds():.2f}s)")
        elif request.node.rep_call.skipped:
            result_status = "SKIPPED"
            test_logger.info(f"⏭️ TEST SKIPPED: {request.node.name} (Duration: {duration.total_seconds():.2f}s)")

    test_logger.info("*" * 60)


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Flight Booking Automation Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Customize HTML report summary"""
    prefix.extend([f"<p>Test Environment: Qantas Flight Booking System</p>"])
    prefix.extend([f"<p>Test Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Setup hook to ensure clean state before each test"""
    logger.info(f"Setting up test: {item.name}")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    """Teardown hook to clean up after each test"""
    logger.info(f"Tearing down test: {item.name}")
    yield