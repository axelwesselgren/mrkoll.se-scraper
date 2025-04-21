from data.user import UserPreview
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests, re, time, random
from config.urls import URLs
from view.logger import Logger
from .checker import Checker
from .parser import Parser

class Scraper:
    ENCODING = "utf-8"
    MAX_TRIES = 5
    
    def __init__(self, model):
        self.model = model
        
        self.tries = 0
        
        self.session = requests.Session()
        self.session.headers = {'User-Agent': UserAgent().random}
       
    def debug(self, message):
        if self.model.debug:
            Logger.info(message)
           
    def get_response(self, url):
        self.debug(f"Reaching: {url}")
        return self.session.get(url)
    
    def search_profiles(self) -> list:
        url = self.model.search.get_main_url()
        response = self.get_response(url)
        checker = Checker(response)
        
        if checker.page_is_empty() or checker.is_forbidden():
            Logger.warning("No results" if checker.page_is_empty() else "Only Swedish IPs allowed")
            return False
            
        return self.load_next_page()
    
    def load_profile(self):
        response = self.get_response(self.model.search.get_user_url())
        
        if Checker(response).is_forbidden():
            Logger.warning("Only Swedish IPs allowed")
            return False
        
        return True
   
    def load_next_page(self) -> list:
        self.debug(f"Loading index [{self.model.current_page}] attempt [{self.tries}]")
        url = f"{URLs.RESULT_URL}{self.model.current_page}"
        response = self.get_response(url)
        checker = Checker(response)
       
        if checker.is_forbidden():
            Logger.warning("Only Swedish IPs allowed")
            return False
            
        if response.url == URLs.BASE_URL:
            Logger.warning("No people found, use a broader search term")
            return False
            
        response.encoding = self.ENCODING
        
        if checker.page_is_empty():
            self.tries += 1
           
            if self.tries == self.MAX_TRIES:
                self.debug("Failed, attempt limit reached")
                Logger.warning("No results > Refine search | Wait a bit | No more pages")
                return False
           
            self.retry()
            return self.load_next_page()
       
        soup = BeautifulSoup(response.text, "html.parser")
        people = soup.find_all('a')
       
        for person in people:
            parser = Parser(person)
            address, zip, city, lived_here = parser.get_address_details()
                       
            self.model.results_preview.append(UserPreview(
                parser.get_name(),
                parser.get_age(),
                address,
                zip,
                city,
                parser.get_birthday(),
                lived_here,
                parser.get_gender(),
                parser.get_pid()
            ))
        
        return self.model.results_preview
        
    def retry(self):
        delay = random.uniform(2, 10)
        self.debug(f"Failed, retrying in {delay} seconds")
        time.sleep(delay)