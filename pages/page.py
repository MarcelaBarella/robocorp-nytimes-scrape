from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

class Page:
    def __init__(self, webdriver: WebDriver = None):
        if (webdriver != None):
            self.webdriver = webdriver
        else:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-impl-side-painting")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("disable-infobars")
            self.webdriver = Chrome(options=options)

    def open(self, url):
        self.webdriver.get(url)

    def close_browser(self):
        self.webdriver.quit()