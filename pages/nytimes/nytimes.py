from pages.page import Page
from pages.nytimes.results import Results
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class NYTimes(Page):

    URL = "https://www.nytimes.com"

    SEARCH_BUTTON_SELECTOR = '[data-test-id="search-button"]'
    SEARCH_INPUT_SELECTOR = '[data-testid="search-input"]'
    SEARCH_SUBMIT_SELECTOR = '[data-test-id="search-submit"]'
    GDPR_ACCEPT_SELECTOR = '[data-testid="GDPR-accept"]'
    GDPR_DOCK = '[data-testid="gdpr-dock"]'

    def open(self):
        super().open(self.URL)

    def accept_gdpr(self):
        gdpr_dock = self.webdriver.find_element(By.CSS_SELECTOR, self.GDPR_DOCK)
        self.webdriver.find_element(By.CSS_SELECTOR, self.GDPR_ACCEPT_SELECTOR).click()
        waiter = WebDriverWait(self.webdriver, 5)
        waiter.until(lambda webdriver: not "show" in gdpr_dock.get_attribute("class"))

    def search(self, term):
        self.webdriver.find_element(By.CSS_SELECTOR, self.SEARCH_BUTTON_SELECTOR).click()
        self.webdriver.find_element(By.CSS_SELECTOR, self.SEARCH_INPUT_SELECTOR).send_keys(term)
        self.webdriver.find_element(By.CSS_SELECTOR, self.SEARCH_SUBMIT_SELECTOR).click()
        return Results(self.webdriver);
