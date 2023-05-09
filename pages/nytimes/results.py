from pages.page import Page
from pages.nytimes.article import Article
from SeleniumLibrary.errors import ElementNotFound


class Results(Page):

    ARTICLES_CONTAINER_CSS_SELECTOR = '[data-testid="search-results"]'
    SECTION_CHECKBOX_CSS_SELECTOR = 'input[type="checkbox"]'

    ARTICLES_LOCATOR = 'data:testid:search-bodega-result'
    SORT_BY_LOCATOR = 'data:testid:SearchForm-sortBy'
    SECTION_DROPDOWN_LOCATOR = 'data:testid:section'
    SHOW_MORE_LOCATOR = 'data:testid:search-show-more-button'

    def sort_by(self, by):
        self.wait_for_articles_to_load(
            lambda: self.webdriver.select_from_list_by_value(
                self.SORT_BY_LOCATOR, by))

    def filter_sections(self, sections):
        dropdown_element = self.webdriver.find_element(
            self.SECTION_DROPDOWN_LOCATOR)
        self.webdriver.click_element(self.SECTION_DROPDOWN_LOCATOR)
        for section in sections:
            # Identify the checkbox element to click by
            # the start of the value property
            checkbox_locator = [
                dropdown_element,
                (f'css:{self.SECTION_CHECKBOX_CSS_SELECTOR}' +
                 f'[value^="{section}|"]')]
            if self.webdriver.is_element_visible(checkbox_locator):
                self.wait_for_articles_to_load(
                    lambda: self.webdriver.click_element(checkbox_locator))

    def wait_for_articles_to_load(self, action):

        # Saves the combined text of current articles in a global variable
        self.webdriver.execute_javascript(
            f"window.initial_articles_content =\
                  document.querySelector('{self.ARTICLES_CONTAINER_CSS_SELECTOR}')\
                    .innerText")

        # Runs the action
        action()

        try:
            # Wait until articles have changed
            # (comparing innerText property of the container)
            self.webdriver.wait_for_condition(
                f"return document.querySelector(\
                    '{self.ARTICLES_CONTAINER_CSS_SELECTOR}').innerText\
                          != window.initial_articles_content")
        except AssertionError:
            # A timeout might happen if the filter/sort applied has no effect
            # on the list of articles and it shouldn't halt the scrapping
            pass

    def load_more_articles(self):
        try:
            self.wait_for_articles_to_load(
                lambda: self.webdriver.click_element(self.SHOW_MORE_LOCATOR))
            return True
        except ElementNotFound:
            # Returns False if there are no more articles to load
            return False

    @property
    def articles(self):
        articles = []
        article_elements = self.webdriver.find_elements(self.ARTICLES_LOCATOR)
        for article_element in article_elements:
            article = Article(self.webdriver, article_element)
            articles.append({
                "title": article.title,
                "date": article.date,
                "description": article.description,
                "picture_url": article.picture_url
            })
        return articles
