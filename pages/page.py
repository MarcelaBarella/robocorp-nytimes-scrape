from RPA.Browser.Selenium import Selenium

class Page:
    def __init__(self, webdriver: Selenium = None):
        if (webdriver != None):
            self.webdriver = webdriver
        else:
            self.webdriver = Selenium()

    def open(self, url):
        self.webdriver.open_available_browser(url)

    def close_browser(self):
        self.webdriver.close_browser()