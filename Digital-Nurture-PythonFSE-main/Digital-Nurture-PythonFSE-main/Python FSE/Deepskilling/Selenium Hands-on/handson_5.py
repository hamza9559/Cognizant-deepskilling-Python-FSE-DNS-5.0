"""
================================================================================
Hands-On 5: Locators & Explicit Wait Mechanisms
================================================================================
Locator Ranking (Most to Least Preferred) for Maintainable Automation:
1. By.ID: Unique, direct, fastest execution time, and highly resistant to HTML changes.
2. By.NAME: Highly unique and stable for processing form structures.
3. By.CSS_SELECTOR: Extremely fast, versatile, and standard for styling targets.
4. By.XPATH (Relative): Powerful layout engine; essential for matching UI text paths.
5. By.CLASS_NAME: Fragile on its own as multiple layout items often share styles.
6. By.TAG_NAME: Too broad on its own; generally only used to parse large tables/lists.
================================================================================
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def run_locator_showcase():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")
        
        # Give the page a quick moment to stabilize in the DOM
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-message")))
        
        # Task 1.32: Demonstrating 6 different locator strategies on the same element
        el_id   = driver.find_element(By.ID, "user-message")
        el_name = driver.find_element(By.NAME, "message")
        el_class= driver.find_element(By.CLASS_NAME, "form-control")
        el_tag  = driver.find_elements(By.TAG_NAME, "input")[2] # Positional fallback
        
        # FIXED: Updated absolute path matching the current LambdaTest DOM tree layout
        el_xp_a = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/div/div/div/div[1]/div[2]/form/div/input")
        el_xp_r = driver.find_element(By.XPATH, "//input[@id='user-message']")
        
        # Task 1.33: 3 distinct CSS Selector strategies for the same element
        css_by_id     = driver.find_element(By.CSS_SELECTOR, "#user-message")
        css_by_attr   = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Please enter your Message']")
        css_by_parent = driver.find_element(By.CSS_SELECTOR, "div.form-group > input")
        
        print("[SUCCESS] All core strategies successfully mapped the message input.")
        
        # Task 1.34: XPath text() and contains() strategies
        driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Option 1']")))
        
        label_exact    = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        label_contains = driver.find_elements(By.XPATH, "//label[contains(text(), 'Option')]")
        print(f"[SUCCESS] Found {len(label_contains)} dynamic labels via contains() syntax.")
        
    finally:
        driver.quit()

def run_waits_showcase():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-demo")
        
        # Task 2.36 & 2.37: Timing explicit waits vs time.sleep()
        start_time = time.time()
        driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        
        alert_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert_div.text.lower()
        print(f"[SUCCESS] Explicit wait completed dynamically in {time.time() - start_time:.3f} seconds.")
        
        # Task 2.38: EC.element_to_be_clickable explanation
        autoclose_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "autoclosable-btn-success"))
        )
        autoclose_btn.click()
        
        # Task 2.39: Fluent Wait implementation using WebDriverWait parameters
        driver.get("https://www.lambdatest.com/selenium-playground/table-sort-search-demo")
        fluent_wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5, ignored_exceptions=[NoSuchElementException])
        
        table_cell = fluent_wait.until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='example']/tbody/tr[1]/td[1]"))
        )
        print(f"[SUCCESS] Fluent Wait verified target element text: '{table_cell.text}'")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("--- Running Locator Strategies Showcase ---")
    run_locator_showcase()
    print("\n--- Running Wait Verification Showcase ---")
    run_waits_showcase()