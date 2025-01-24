from src.adapters import OSClient, RequestsClient, SeleniumClient
from src.collector import Collector

def execute_scraper():
    try:
        os_client = OSClient()
        requests_client = RequestsClient()
        selenium_client = SeleniumClient()
        
        collector = Collector(os_client, requests_client, selenium_client)
        collector.collect()
           
    except Exception as e:
        print(f"Unexpected error : {e}")