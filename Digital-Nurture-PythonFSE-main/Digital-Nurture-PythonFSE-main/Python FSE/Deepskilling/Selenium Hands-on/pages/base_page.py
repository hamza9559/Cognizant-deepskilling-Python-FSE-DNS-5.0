from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url):
        self.driver.get(url)

    def navigate_to_safe(self, url, check_locator, retries=3):
        import time
        for i in range(retries):
            try:
                self.driver.get(url)
                time.sleep(2)
                self.wait_for_element(check_locator)
                return
            except Exception as e:
                if i == retries - 1:
                    raise e
                time.sleep(2)

    def get_title(self):
        return self.driver.title

    def wait_for_element(self, locator, timeout=10):
        """
        Wait for an element to be present in the DOM.
        :param locator: A tuple of (By, selector)
        :param timeout: Time to wait in seconds
        :return: WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_element_visible(self, locator, timeout=10):
        """
        Wait for an element to be visible on the page.
        :param locator: A tuple of (By, selector)
        :param timeout: Time to wait in seconds
        :return: WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
