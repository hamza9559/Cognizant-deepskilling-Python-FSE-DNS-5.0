"""
================================================================================
Hands-On 4: Selenium WebDriver Setup, Navigation & Basic Commands
================================================================================
QA Concept Answers (Task 1.24):
1. WebDriver: Communicates directly with browsers using native W3C protocol commands.
2. Selenium Grid: Solves the problem of scaling by running tests in parallel across multiple machines/browsers.
3. Selenium IDE: A record-and-playback browser extension used for rapid prototyping.
================================================================================
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_headless_check():
    # Task 1.27: Headless Mode configuration
    options = Options()
    options.add_argument('--headless')
    
    # Task 1.25: Initializing Chrome via webdriver-manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    # Task 1.26: Why global implicit wait is bad practice
    # Setting an implicit wait globally applies to every single element search. 
    # It can hide performance issues and drastically slow down tests when you are 
    # intentionally waiting or asserting that an element should NOT be present on the page.
    driver.implicitly_wait(10)
    
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/")
        print(f"[SUCCESS] Headless Title Verified: {driver.title}")
    finally:
        driver.quit()

def run_navigation_and_windows():
    # Regular interactive browser window
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    try:
        # Task 2.28: Navigation & URL assertion
        driver.get("https://www.lambdatest.com/selenium-playground/")
        driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
        
        assert "simple-form-demo" in driver.current_url, f"URL Assertion failed! Found: {driver.current_url}"
        print("[SUCCESS] URL verification matched expected page path.")
        
        driver.back()
        
        # Task 2.29: Open a new tab and switch to it
        driver.execute_script('window.open("https://www.google.com");')
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        print(f"[SUCCESS] Secondary Tab Title: {driver.title}")
        
        # Task 2.30: Switch back and take a screenshot
        driver.switch_to.window(handles[0])
        driver.save_screenshot('playground_screenshot.png')
        print("[SUCCESS] Original window screenshot captured as 'playground_screenshot.png'.")
        
        # Task 2.31: Window sizing setting & explanation
        # Setting a consistent window size is critical for responsive UI testing. 
        # If the browser scales down dynamically, elements might hide behind hamburger menus, 
        # changing the page layout and causing elements to become unclickable.
        driver.set_window_size(1280, 800)
        print(f"[SUCCESS] Active window size locked to: {driver.get_window_size()}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("--- Starting Headless Check ---")
    run_headless_check()
    print("\n--- Starting Navigation & Window Suite ---")
    run_navigation_and_windows()