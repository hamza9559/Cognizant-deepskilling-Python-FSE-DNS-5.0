from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SimpleFormPage(BasePage):
    # Class-level locators
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Get Checked Value')]")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        input_field = self.wait_for_element(self.MESSAGE_INPUT)
        input_field.clear()
        input_field.send_keys(text)
        return self

    def click_submit(self):
        submit_btn = self.wait_for_element(self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].click();", submit_btn)
        return self

    def get_displayed_message(self):
        message_el = self.wait_for_element_visible(self.DISPLAYED_MESSAGE)
        return message_el.text
