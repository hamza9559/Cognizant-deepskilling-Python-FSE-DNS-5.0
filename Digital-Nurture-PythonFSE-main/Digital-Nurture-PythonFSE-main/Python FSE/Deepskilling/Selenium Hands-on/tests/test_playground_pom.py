import pytest
import time
from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage

@pytest.mark.parametrize('message', ['Hello', 'Selenium Automation', '12345'])
def test_simple_form_submission(driver, base_url, message):
    # Step 55: Use SimpleFormPage page object class with safe navigation
    page = SimpleFormPage(driver)
    page.navigate_to_safe(base_url + 'simple-form-demo/', page.MESSAGE_INPUT)
    
    page.enter_message(message)
    page.click_submit()
    
    # Click retry loop for robust async behavior
    for _ in range(3):
        try:
            assert page.get_displayed_message() == message
            break
        except Exception:
            page.click_submit()
            time.sleep(1)
            
    # Final assertion verification
    assert page.get_displayed_message() == message

def test_checkbox_demo(driver, base_url):
    # Step 56: Use CheckboxPage
    page = CheckboxPage(driver)
    page.navigate_to_safe(base_url + 'checkbox-demo/', page._get_option_locator(1))
    
    # Check option 1
    page.check_option(1)
    assert page.is_option_checked(1)
    
    # Uncheck option 1
    page.uncheck_option(1)
    assert not page.is_option_checked(1)

def test_dropdown_selection(driver, base_url):
    # Step 56: Use DropdownPage
    page = DropdownPage(driver)
    page.navigate_to_safe(base_url + 'select-dropdown-demo/', page.DROPDOWN_SELECT)
    
    page.select_day('Wednesday')
    assert page.get_selected_day() == 'Wednesday'

def test_input_form_submit(driver, base_url):
    # Step 57: Use InputFormPage
    page = InputFormPage(driver)
    page.navigate_to_safe(base_url + 'input-form-demo/', page.NAME_INPUT)
    
    # Fill dynamic fields and submit
    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="456 Test Lane"
    )
    page.submit_form()
    
    # Assert successful submit message
    success_text = page.get_success_message()
    assert "Thanks for contacting us" in success_text
