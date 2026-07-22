from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckboxPage(BasePage):
    def _get_option_locator(self, index):
        # Dynamically build locator based on Option text (e.g. Option 1, Option 2)
        return (By.XPATH, f"//label[contains(text(), 'Option {index}')]/input")

    def check_option(self, index):
        locator = self._get_option_locator(index)
        checkbox = self.wait_for_element(locator)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def uncheck_option(self, index):
        locator = self._get_option_locator(index)
        checkbox = self.wait_for_element(locator)
        if checkbox.is_selected():
            checkbox.click()
        return self

    def is_option_checked(self, index):
        locator = self._get_option_locator(index)
        checkbox = self.wait_for_element(locator)
        return checkbox.is_selected()
