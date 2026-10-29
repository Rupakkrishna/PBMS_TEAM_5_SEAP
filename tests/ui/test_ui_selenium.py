"""
PB-23: Automated Key UI Workflow Test using Selenium Headless Chrome
Workflow:
1. Customer Login (login.html)
2. View Customer Dashboard (user/dashboard.html)
3. Search and select an available bicycle (PB-11)
4. Confirm bicycle rental (PB-12)
5. Verify active rental duration counter & banner (PB-14, PB-15)
6. Return bicycle to destination docking station (PB-16, PB-07)
7. Verify calculated fare and simulated payment ledger status (PB-15, PB-17)
"""

import os
import sys
import time
import threading
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database.db import init_db_schema
from backend.database.seed import seed_database

TEST_PORT = 5055
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"

@pytest.fixture(scope="module")
def live_server():
    """Start local Flask server in background thread using dedicated test database."""
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['USE_SQLITE_TEST'] = 'true'
    test_db = os.path.abspath(os.path.join(os.path.dirname(__file__), 'selenium_test.sqlite'))
    os.environ['SQLITE_DB_PATH'] = test_db

    app = create_app('testing')

    with app.app_context():
        init_db_schema()
        seed_database()

    # Start server thread
    import werkzeug.serving
    server = werkzeug.serving.make_server('127.0.0.1', TEST_PORT, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(1)  # Allow server to bind

    yield BASE_URL

    server.shutdown()
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass

@pytest.fixture(scope="module")
def browser():
    """Initialize Selenium Headless Chrome."""
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,900')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()

def test_selenium_key_ui_workflow(live_server, browser):
    """
    PB-23 End-to-End Workflow:
    Login -> Search Available Bikes -> Rent Bike -> Return Bike -> Check Fare & Payment
    """
    wait = WebDriverWait(browser, 12)

    # 1. Open Login Page
    browser.get(f"{live_server}/login.html")
    assert "Sign In" in browser.title

    # 2. Authenticate as Customer with no active rental (Bob)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    password_field = browser.find_element(By.ID, "password")
    submit_btn = browser.find_element(By.ID, "loginSubmitBtn")

    email_field.clear()
    email_field.send_keys("bob@example.com")
    password_field.clear()
    password_field.send_keys("User@123")
    submit_btn.click()

    # 3. Verify Customer Dashboard redirect
    wait.until(EC.url_contains("/user/dashboard.html"))
    assert "/user/dashboard.html" in browser.current_url

    # 4. Search and verify available bicycles (PB-11)
    wait.until(EC.presence_of_element_located((By.ID, "bicyclesList")))
    
    # Wait until "Rent Now" button is clickable
    rent_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Rent Now')]")))
    assert rent_btn is not None

    # Click first available Rent button
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", rent_btn)
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", rent_btn)

    # 5. Confirm Rental in Modal (PB-12)
    confirm_btn = wait.until(EC.element_to_be_clickable((By.ID, "confirmRentBtn")))
    browser.execute_script("arguments[0].click();", confirm_btn)

    # 6. Verify Active Rental Banner appeared (PB-14, PB-15)
    active_banner = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "active-rental-banner")))
    assert active_banner is not None
    assert "ACTIVE RENTAL" in active_banner.text

    # 7. Return Bicycle (PB-16, PB-07)
    time.sleep(1)
    return_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Return Bike')]")))
    browser.execute_script("arguments[0].click();", return_btn)

    # Wait for return modal & select return station
    return_station_select = wait.until(EC.presence_of_element_located((By.ID, "returnStationSelect")))
    time.sleep(0.5)
    # Select destination station via JavaScript (avoids bootstrap animation lock)
    browser.execute_script("""
        const select = arguments[0];
        for (let i = 0; i < select.options.length; i++) {
            if (!select.options[i].disabled && select.options[i].value) {
                select.selectedIndex = i;
                select.dispatchEvent(new Event('change'));
                break;
            }
        }
    """, return_station_select)

    confirm_return_btn = wait.until(EC.presence_of_element_located((By.ID, "confirmReturnBtn")))
    browser.execute_script("arguments[0].click();", confirm_return_btn)

    # 8. Verify Fare Receipt Modal and Simulated Payment Status (PB-15, PB-17)
    wait.until(lambda d: d.find_element(By.ID, "receiptFare").text not in ["", "-"])
    receipt_fare = browser.find_element(By.ID, "receiptFare")
    assert "₹" in receipt_fare.text, "Fare should contain Indian Rupee currency symbol (₹)"

    wait.until(lambda d: "Paid" in d.find_element(By.ID, "receiptPaymentStatus").text)
    receipt_payment = browser.find_element(By.ID, "receiptPaymentStatus")
    assert "Paid" in receipt_payment.text, "Payment status should be Paid (Simulated)"
