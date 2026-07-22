import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Ensure the root folder is in python path so that 'pages' package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    
    # Teardown
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver):
    yield
    # Capture screenshot if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name
        # Clean the test name to create a safe file name
        clean_name = "".join([c if c.isalnum() or c in ('_', '-') else '_' for c in test_name])
        screenshot_path = f"{clean_name}_failure.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[FAILURE] POM Test '{test_name}' failed. Screenshot saved to: {screenshot_path}")
