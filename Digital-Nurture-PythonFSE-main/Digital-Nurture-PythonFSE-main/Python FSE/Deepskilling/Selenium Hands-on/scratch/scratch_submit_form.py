import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1280,1020')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.lambdatest.com/selenium-playground/input-form-demo")
    time.sleep(3)
    
    driver.find_element(By.ID, "name").send_keys("Jane Doe")
    driver.find_element(By.ID, "inputEmail4").send_keys("jane.doe@example.com")
    driver.find_element(By.ID, "inputPassword4").send_keys("Password123")
    driver.find_element(By.ID, "company").send_keys("9876543210")
    driver.find_element(By.ID, "websitename").send_keys("https://example.com")
    
    select_el = driver.find_element(By.NAME, "country")
    Select(select_el).select_by_visible_text("United States")
    
    driver.find_element(By.ID, "inputCity").send_keys("San Francisco")
    driver.find_element(By.ID, "inputAddress1").send_keys("456 Test Lane")
    driver.find_element(By.ID, "inputAddress2").send_keys("Suite 100")
    driver.find_element(By.ID, "inputState").send_keys("California")
    driver.find_element(By.ID, "inputZip").send_keys("94105")
    
    print("Form filled. Submitting...")
    
    # Try clicking the submit button
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    print("Submit button text:", submit_btn.text)
    print("Submit button outerHTML:", submit_btn.get_attribute("outerHTML"))
    
    # Click via JS
    driver.execute_script("arguments[0].click();", submit_btn)
    print("JS Click performed.")
    
    time.sleep(3)
    
    # Check for success message presence
    success_els = driver.find_elements(By.CSS_SELECTOR, ".success-msg")
    print(f"Total elements with class .success-msg: {len(success_els)}")
    for i, el in enumerate(success_els):
        print(f"  El {i}: visible={el.is_displayed()}, text='{el.text}', outerHTML='{el.get_attribute('outerHTML')}'")
        
    # Check if there is any validation message active on any input
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for inp in inputs:
        validation_message = driver.execute_script("return arguments[0].validationMessage;", inp)
        if validation_message:
            print(f"  Input id='{inp.get_attribute('id')}' validationMessage: '{validation_message}'")

finally:
    driver.quit()
