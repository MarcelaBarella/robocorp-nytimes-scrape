from pages.page import Page
from pages.nytimes.results import Results


class NYTimes(Page):

    URL = "https://www.nytimes.com"

    GDPR_DOCK_CSS_SELECTOR = '[data-testid="gdpr-dock"]'

    SEARCH_BUTTON_LOCATOR = 'data:test-id:search-button'
    SEARCH_INPUT_LOCATOR = 'data:testid:search-input'
    SEARCH_SUBMIT_LOCATOR = 'data:test-id:search-submit'
    GDPR_ACCEPT_LOCATOR = 'data:testid:GDPR-accept'
    GDPR_DOCK_LOCATOR = f'css:{GDPR_DOCK_CSS_SELECTOR}'

    def open(self):
        super().open(self.URL)

    def accept_gdpr(self):
        self.webdriver.click_element(self.GDPR_ACCEPT_LOCATOR)
        self.webdriver.wait_for_condition(
            f"return !document.querySelector('{self.GDPR_DOCK_CSS_SELECTOR}')\
                .classList.contains('show')")

    def search(self, term):
        self.webdriver.click_element(self.SEARCH_BUTTON_LOCATOR)
        self.webdriver.press_keys(self.SEARCH_INPUT_LOCATOR, term)
        self.webdriver.click_element(self.SEARCH_SUBMIT_LOCATOR)
        return Results(self.webdriver)
