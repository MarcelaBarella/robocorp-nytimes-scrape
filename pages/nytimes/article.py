from datetime import datetime
from selenium.webdriver.common.by import By

class Article:
    TITLE_SELECTOR = 'h4'
    DATE_SELECTOR = '[data-testid="todays-date"]'
    DESCRIPTION_SELECTOR = 'h4 + p'
    PICTURE_SELECTOR = 'figure img'

    def __init__(self, article_element):
        self.article_element = article_element
    
    @property
    def title(self):
        try:
            return self.article_element.find_element(By.CSS_SELECTOR, self.TITLE_SELECTOR).text
        except:
            return ''
    
    @property
    def date(self):
        try:
            date_text = self.article_element.find_element(By.CSS_SELECTOR, self.DATE_SELECTOR).get_attribute("aria-label")
            if not "," in date_text:
                date_text = date_text + f", {datetime.now().year}"
            return datetime.strptime(date_text, "%B %d, %Y").date().strftime("%Y-%m-%d")
        except:
            return ''
    
    @property
    def description(self):
        try:
            return self.article_element.find_element(By.CSS_SELECTOR, self.DESCRIPTION_SELECTOR).text
        except:
            return ''
    
    @property
    def picture_url(self):
        try:
            return self.article_element.find_element(By.CSS_SELECTOR, self.PICTURE_SELECTOR).get_attribute("src")
        except:
            return ''