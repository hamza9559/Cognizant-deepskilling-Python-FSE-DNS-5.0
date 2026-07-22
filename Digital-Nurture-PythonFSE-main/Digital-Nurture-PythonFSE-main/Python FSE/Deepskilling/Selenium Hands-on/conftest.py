import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='session')
def base_url():
    return 'https://www.lambdatest.com/selenium-playground/'

@pytest.fixture(scope='function')
def driver():
    # Configure Chrome options
    options = Options()
    options.add_argument('--headless')  # Run headless for automated test execution
    options.add_argument('--window-size=1280,800')
    # Add anti-detection flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Initialize driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Teardown: close the driver after the test
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # Set a report attribute for each phase of a call ("setup", "call", "teardown")
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver):
    yield
    # Check if request.node.rep_call exists and if it failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name
        # Clean the test name to create a safe file name
        clean_name = "".join([c if c.isalnum() or c in ('_', '-') else '_' for c in test_name])
        screenshot_path = f"{clean_name}_failure.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[FAILURE] Test '{test_name}' failed. Screenshot saved to: {screenshot_path}")
        
        # Retrieve and print browser console logs
        try:
            logs = driver.get_log('browser')
            print("\n--- BROWSER CONSOLE LOGS ---")
            for entry in logs:
                print(f"{entry['level']}: {entry['message']}")
            print("----------------------------")
        except Exception as e:
            print(f"Could not retrieve console logs: {e}")
