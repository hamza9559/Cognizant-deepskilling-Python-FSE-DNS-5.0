import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

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
    
    print("Page Title:", driver.title)
    
    # List all input fields
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"Total inputs on input-form-demo: {len(inputs)}")
    for i, inp in enumerate(inputs):
        print(f"  Input {i}: id='{inp.get_attribute('id')}', name='{inp.get_attribute('name')}', placeholder='{inp.get_attribute('placeholder')}', required='{inp.get_attribute('required')}'")
        
    # List all select elements
    selects = driver.find_elements(By.TAG_NAME, "select")
    print(f"Total selects: {len(selects)}")
    for i, sel in enumerate(selects):
        print(f"  Select {i}: id='{sel.get_attribute('id')}', name='{sel.get_attribute('name')}'")
        
    # List all buttons
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"Total buttons: {len(buttons)}")
    for i, btn in enumerate(buttons):
        print(f"  Button {i}: id='{btn.get_attribute('id')}', text='{btn.text}'")

finally:
    driver.quit()
