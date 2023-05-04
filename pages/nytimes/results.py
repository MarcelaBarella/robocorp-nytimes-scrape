from datetime import datetime
from pages.page import Page
from pages.nytimes.article import Article
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class Results(Page):

    ARTICLES_SELECTOR = '[data-testid="search-bodega-result"]'
    SORT_BY_SELECTOR = '[data-testid="SearchForm-sortBy"]'
    SECTION_DROPDOWN_SELECTOR = '[data-testid="section"]'
    SECTION_CHECKBOX_SELECTOR = 'input[type="checkbox"]'
    SHOW_MORE_SELECTOR = '[data-testid="search-show-more-button"]'

    def sort_by(self, by):
        select_element = self.webdriver.find_element(By.CSS_SELECTOR, self.SORT_BY_SELECTOR)
        select = Select(select_element)

        if select.first_selected_option == by:
            # Already sorted by the right criteria, return
            return
        
        self.wait_for_articles_to_load(lambda: select.select_by_value(by))
    
    def filter_sections(self, sections):
        sections_dropdown = self.webdriver.find_element(By.CSS_SELECTOR, self.SECTION_DROPDOWN_SELECTOR)
        sections_dropdown.click()
        for section in sections:
            try:
                self.wait_for_articles_to_load(lambda: sections_dropdown.find_element(By.CSS_SELECTOR, self.SECTION_CHECKBOX_SELECTOR + f'[value^="{section}|"]').click())
            except NoSuchElementException:
                # Section might not exist for an specific search term
                pass
        

    def wait_for_articles_to_load(self, func):
        initial_articles = self.webdriver.find_element(By.CSS_SELECTOR, self.ARTICLES_SELECTOR).text
        func()
        waiter = WebDriverWait(self.webdriver, 5)
        try:
            waiter.until(lambda webdriver: webdriver.find_element(By.CSS_SELECTOR, self.ARTICLES_SELECTOR).text != initial_articles)
        except:
            # A timeout might happen if the filter/sort applied has no effect on the list of articles
            # and it shouldn't halt the scrapping
            pass

    def load_more_articles(self):
        try:
            print("load_more_articles")
            show_more = self.webdriver.find_element(By.CSS_SELECTOR, self.SHOW_MORE_SELECTOR)
            self.wait_for_articles_to_load(lambda: show_more.click())
            return True
        except Exception as e:
            print("load_more_articles exception")
            print(e)
            # Returns False if there are no more articles to load
            return False

    @property
    def articles(self):
        articles = []
        article_elements = self.webdriver.find_elements(By.CSS_SELECTOR, self.ARTICLES_SELECTOR)
        for article_element in article_elements:
            article = Article(article_element)
            articles.append({
                "title": article.title,
                "date": article.date,
                "description": article.description,
                "picture_url": article.picture_url
            })
        return articles
