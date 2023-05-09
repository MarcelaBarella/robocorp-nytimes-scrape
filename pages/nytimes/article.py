from datetime import datetime
from RPA.Browser.Selenium import Selenium

class Article:
    TITLE_LOCATOR = 'tag:h4'
    DATE_LOCATOR = 'css:[data-testid="todays-date"]'
    DESCRIPTION_LOCATOR = 'css:h4 + p'
    PICTURE_LOCATOR = 'css:figure img'

    def __init__(self, webdriver: Selenium, article_element):
        self.article_element = article_element
        self.webdriver = webdriver
    
    @property
    def title(self):
        try:
            return self.webdriver.get_text([self.article_element, self.TITLE_LOCATOR])
        except:
            return ''
    
    @property
    def date(self):
        try:
            date_text = self.webdriver.get_element_attribute([self.article_element, self.DATE_LOCATOR], "aria-label")
            if not "," in date_text:
                date_text = date_text + f", {datetime.now().year}"
            return datetime.strptime(date_text, "%B %d, %Y").date().strftime("%Y-%m-%d")
        except:
            return ''
    
    @property
    def description(self):
        try:
            return self.webdriver.get_text([self.article_element, self.DESCRIPTION_LOCATOR])
        except:
            return ''
    
    @property
    def picture_url(self):
        try:
            return self.webdriver.get_element_attribute([self.article_element, self.PICTURE_LOCATOR], "src")
        except:
            return ''