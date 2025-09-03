# Qantas Flight Booking Test Framework

Simple Playwright test framework for testing Qantas flight booking functionality.

## Features Implemented

✅ **Page Object Model** - Clean separation of page logic  
✅ **Conftest.py** - Browser setup and configuration  
✅ **PyTest Marks** - Smoke and regression test categorization  
✅ **Pytest Rerun** - Automatic retry on test failures  
✅ **Default Timeout** - 30-second timeout configuration  
✅ **Workers** - Parallel test execution support  
✅ **Reusable Methods** - Page object methods for common actions  
✅ **Relative XPaths** - Playwright locators with XPath selectors  
✅ **Screenshots** - Automatic failure screenshots  
✅ **HTML Reports** - Test results in HTML format  
✅ **JSON Data Reader** - Test data externalized in JSON  

## Project Structure

```
├── conftest.py           # Test configuration and fixtures
├── page_objects.py       # Page Object Model implementation
├── test_data.json        # Test data (origins, destinations, dates)
├── test_case_1.py        # Test Case 1: One-way flight booking
├── test_case_2.py        # Test Case 2: Round-trip flight booking
├── test_case_3.py        # Test Case 3: Missing return date validation
├── test_case_4.py        # Test Case 4: Infant passenger limit validation
├── pytest.ini           # Pytest configuration
├── requirements.txt      # Dependencies
├── run_tests.py         # Test runner script
├── screenshots/         # Failure screenshots (auto-created)
└── reports/             # HTML test reports (auto-created)
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run tests:
```bash
# All tests
python run_tests.py

# Smoke tests only
python run_tests.py smoke

# Regression tests only  
python run_tests.py regression

# Specific test
python run_tests.py testcase1_successful_oneway_flight.py
```

## Test Cases

### Test Case 1: One-Way Flight Booking
- **Objective**: Verify one-way flight booking functionality
- **Mark**: `@pytest.mark.smoke`
- **Steps**: Select origin/destination, departure date, search flights

### Test Case 2: Round-Trip Flight Booking  
- **Objective**: Verify round-trip flight booking functionality
- **Mark**: `@pytest.mark.regression`
- **Steps**: Select origin/destination, departure/return dates, search flights

### Test Case 3: Missing Return Date Validation
- **Objective**: Verify error when return date is missing for round-trip
- **Mark**: `@pytest.mark.regression`  
- **Steps**: Select round-trip without return date, verify error message

### Test Case 4: Infant Passenger Limit
- **Objective**: Verify 1 infant per adult limitation
- **Mark**: `@pytest.mark.smoke`
- **Steps**: Add infant passenger, verify plus button disabled and error shown

## Configuration

- **Browser**: Chromium (maximized, slow motion enabled)
- **Timeout**: 30 seconds default
- **Reruns**: 1 automatic retry on failure
- **Workers**: 2 parallel workers
- **Screenshots**: Automatic on test failure
- **Reports**: HTML format in `reports/` directory

## Test Data

All test data is externalized in `test_data.json`:
- Origins and destinations
- Departure/return dates
- Passenger counts
- Expected error messages

This keeps tests maintainable and data-driven.