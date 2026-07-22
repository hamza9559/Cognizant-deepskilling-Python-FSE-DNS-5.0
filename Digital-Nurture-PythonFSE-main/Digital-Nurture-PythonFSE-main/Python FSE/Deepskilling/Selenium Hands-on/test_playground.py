import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def safe_get(driver, url, check_locator, retries=3):
    """
    Robust page loader with automatic retry on network reset/errors
    """
    for i in range(retries):
        try:
            driver.get(url)
            # Short sleep to allow dynamic assets to load and DOM to settle
            time.sleep(2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(check_locator)
            )
            return
        except Exception as e:
            if i == retries - 1:
                raise e
            print(f"\n[RETRY] Attempt {i+1} failed to load {url}. Retrying...")
            time.sleep(2)

@pytest.mark.parametrize('message', ['Hello', 'Selenium Automation', '12345'])
def test_simple_form_submission(driver, base_url, message):
    # Step 42: Open the Simple Form Demo using trailing slash and safe_get
    safe_get(driver, base_url + 'simple-form-demo/', (By.ID, "user-message"))
    
    msg_input = driver.find_element(By.ID, "user-message")
    
    # Enter the message
    msg_input.clear()
    msg_input.send_keys(message)
    
    # Click the Submit button (Get Checked Value)
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "showInput"))
    )
    
    # Try normal click, fallback to JS click if needed
    try:
        submit_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", submit_btn)
    
    # Wait for the displayed message element to contain our input text
    # We do a retry loop for the click itself if the text update doesn't happen instantly
    for _ in range(3):
        try:
            WebDriverWait(driver, 3).until(
                EC.text_to_be_present_in_element((By.ID, "message"), message)
            )
            break
        except Exception:
            # Re-click if event listener failed to fire first time
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(1)
            
    # Assert the text matches
    displayed_msg_el = driver.find_element(By.ID, "message")
    assert displayed_msg_el.text == message

def test_checkbox_demo(driver, base_url):
    # Step 43: Open the Checkbox Demo
    option1_xpath = "//label[contains(text(), 'Option 1')]/input"
    safe_get(driver, base_url + 'checkbox-demo/', (By.XPATH, option1_xpath))
    
    checkbox = driver.find_element(By.XPATH, option1_xpath)
    
    # Ensure it starts deselected
    if checkbox.is_selected():
        checkbox.click()
        
    # Click the checkbox
    checkbox.click()
    # Assert it is selected
    assert checkbox.is_selected()
    
    # Click it again
    checkbox.click()
    # Assert it is deselected
    assert not checkbox.is_selected()

def test_dropdown_selection(driver, base_url):
    # Step 49: Open the Select Dropdown List demo
    safe_get(driver, base_url + 'select-dropdown-demo/', (By.ID, "select-demo"))
    
    select_el = driver.find_element(By.ID, "select-demo")
    
    # Use Select helper to select 'Wednesday'
    select_obj = Select(select_el)
    select_obj.select_by_visible_text('Wednesday')
    
    # Assert selected option is 'Wednesday'
    selected_option = select_obj.first_selected_option
    assert selected_option.text == 'Wednesday'
