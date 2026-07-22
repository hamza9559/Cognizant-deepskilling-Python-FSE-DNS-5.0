from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class DropdownPage(BasePage):
    # Class-level locator
    DROPDOWN_SELECT = (By.ID, "select-demo")

    def select_day(self, day_name):
        select_el = self.wait_for_element(self.DROPDOWN_SELECT)
        select_obj = Select(select_el)
        select_obj.select_by_visible_text(day_name)
        return self

    def get_selected_day(self):
        select_el = self.wait_for_element(self.DROPDOWN_SELECT)
        select_obj = Select(select_el)
        return select_obj.first_selected_option.text
