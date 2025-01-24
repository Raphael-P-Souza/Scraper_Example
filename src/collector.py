from src.adapters import OSClient, RequestsClient, SeleniumClient
from src import PROJECT_NAME

from decouple import config
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

class Collector():
    
    def __init__(self, osclient : OSClient, requestsclient : RequestsClient, seleniumclient : SeleniumClient):
        self.os_client = osclient
        self.requests_client = requestsclient
        self.selenium_client = seleniumclient

        self.execution_date = datetime.today().strftime("%Y-%m-%d")
        
        self.processed_data_fields = [
            "description",
            "price",
            "localization",
            "date",
        ]
        
        self.metadata = {
            "project_name" : PROJECT_NAME,
            "execution_date" : self.execution_date
        }
        
        #page_link = config("PAGE_LINK", default=None)
        #if not page_link:
        #    raise Exception("Missing environment variable : PAGE_LINK")
    
    def collect(self):
        try:
            term = "guitar giannini"
            
            #raw_data_requests = self.requests_client
            raw_ebay_data_selenium = self.selenium_client.collet_from_ebay(term)
            processed_data = self.process_ebay_data(raw_ebay_data_selenium)
            self.os_client.save_data(processed_data)
            
        except Exception as e:
            print(f"Error found: {e}")
        
    def process_ebay_data(self, raw_data):
        dataframe = pd.DataFrame(columns=self.processed_data_fields)
        
        for data in raw_data:        
            soup = BeautifulSoup(data, "html.parser")
            products = soup.find_all("div", class_="s-item__wrapper clearfix")
            for item in products:
                if item.find("span", class_="s-item__location s-item__itemLocation") is not None:
                    description = item.find("div", class_="s-item__title").text
                    price = item.find("span", class_="s-item__price").text
                    local = item.find("span", class_="s-item__location s-item__itemLocation").text.replace("de ", "")
                    item = {
                        "description" : description,
                        "price" : price,
                        "localization" : local,
                        "date" : self.execution_date
                    }
                    dataframe = pd.concat([dataframe, pd.DataFrame.from_records([item])], ignore_index=True)
        return dataframe