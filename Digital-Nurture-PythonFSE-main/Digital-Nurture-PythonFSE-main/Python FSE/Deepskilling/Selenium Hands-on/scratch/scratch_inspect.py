import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1280,800')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo/")
    time.sleep(3)
    
    # Let's list all input elements
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"Total inputs: {len(inputs)}")
    for idx, inp in enumerate(inputs):
        print(f"  Input {idx}: id='{inp.get_attribute('id')}', name='{inp.get_attribute('name')}', outerHTML='{inp.get_attribute('outerHTML')[:120]}'")
        
    # Let's list all button elements
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"Total buttons: {len(buttons)}")
    for idx, btn in enumerate(buttons):
        print(f"  Button {idx}: id='{btn.get_attribute('id')}', class='{btn.get_attribute('class')}', text='{btn.text}'")
        
    # Let's list all elements with ID 'message'
    messages = driver.find_elements(By.ID, "message")
    print(f"Total elements with ID 'message': {len(messages)}")
    for idx, msg in enumerate(messages):
        print(f"  Message {idx}: tag='{msg.tag_name}', text='{msg.text}', class='{msg.get_attribute('class')}'")

    # Enter text and press ENTER
    print("\nTrying to enter text and press ENTER key...")
    input_el = driver.find_element(By.ID, "user-message")
    input_el.clear()
    input_el.send_keys("Hello via Enter" + Keys.ENTER)
    time.sleep(2)
    
    message_el = driver.find_element(By.ID, "message")
    print(f"Message after Enter: '{message_el.text}'")
    
    # Try clicking the first button that has text "Get Checked Value"
    print("\nClicking button with text 'Get Checked Value'...")
    btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Get Checked Value')]")
    btn.click()
    time.sleep(2)
    print(f"Message after button click: '{message_el.text}'")
    
    # If it still didn't work, let's look at the javascript variables or handlers if possible
    # e.g., is there a javascript function named showInput?
    res = driver.execute_script("return typeof showInput;")
    print(f"Type of showInput in global JS scope: {res}")
    
finally:
    driver.quit()
