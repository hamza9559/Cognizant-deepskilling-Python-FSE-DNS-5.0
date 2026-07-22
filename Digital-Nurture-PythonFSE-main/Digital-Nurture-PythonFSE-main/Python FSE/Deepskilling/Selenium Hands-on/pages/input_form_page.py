from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InputFormPage(BasePage):
    # Class-level locators for all fields on the Input Form Submit page
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "inputEmail4")
    PASSWORD_INPUT = (By.ID, "inputPassword4")
    COMPANY_INPUT = (By.ID, "company")
    WEBSITE_INPUT = (By.ID, "websitename")
    COUNTRY_SELECT = (By.NAME, "country")
    CITY_INPUT = (By.ID, "inputCity")
    ADDRESS1_INPUT = (By.ID, "inputAddress1")
    ADDRESS2_INPUT = (By.ID, "inputAddress2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_INPUT = (By.ID, "inputZip")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg")

    def fill_form(self, name, email, phone, address, password="Password123", website="https://example.com", country="United States", city="San Francisco", state="California", zip_code="94105", address2="Suite 100"):
        """
        Fills out the input form.
        Note: The actual page does not contain a 'phone' field, but contains Password, Company, Website, Country, etc.
        We map 'phone' to the 'Company' field to satisfy the requested signature and use robust defaults 
        for the other required fields so that HTML5 form validation passes successfully.
        """
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.wait_for_element(self.EMAIL_INPUT).send_keys(email)
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_element(self.COMPANY_INPUT).send_keys(phone)  # Map phone to Company field
        self.wait_for_element(self.WEBSITE_INPUT).send_keys(website)
        
        # Select country from the dropdown
        country_el = self.wait_for_element(self.COUNTRY_SELECT)
        select_obj = Select(country_el)
        select_obj.select_by_visible_text(country)
        
        self.wait_for_element(self.CITY_INPUT).send_keys(city)
        self.wait_for_element(self.ADDRESS1_INPUT).send_keys(address)
        self.wait_for_element(self.ADDRESS2_INPUT).send_keys(address2)
        self.wait_for_element(self.STATE_INPUT).send_keys(state)
        self.wait_for_element(self.ZIP_INPUT).send_keys(zip_code)
        return self

    def submit_form(self):
        submit_btn = self.wait_for_element(self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].click();", submit_btn)
        return self

    def get_success_message(self):
        success_el = self.wait_for_element_visible(self.SUCCESS_MESSAGE)
        return success_el.text
