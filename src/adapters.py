from selenium import webdriver
import pandas as pd

class OSClient():
    def __init__(self):
        self.DATAFRAME_PATH = "./data/"
        pass
    
    def save_data(self, data : pd.DataFrame):
        data.to_csv(f"{self.DATAFRAME_PATH}example.csv")
    
class RequestsClient():
    def __init__(self):
        pass
    
class SeleniumClient():
    
    def __init__(self):
        self.webdriver = self.create_webdriver()
        
    def create_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless=new") 
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-gpu") 
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options=options)
        return driver
    
    def enter_url(self, url):
        self.webdriver.get(url=url)
    
    def get_html(self):
        return self.webdriver.page_source
    
    def collet_from_ebay(self, term, pages = 1):
        raw_data_list = []
        url = f"https://www.ebay.com/sch/i.html?_nkw={term.replace(' ', '+')}"
        self.enter_url(url)
        counter = 1
        while counter <= pages:
            raw_data_list.append(self.get_html())
            #Process pages
            counter = counter + 1
            if counter <= pages:
                break
        return raw_data_list