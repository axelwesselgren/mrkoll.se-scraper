from bs4 import BeautifulSoup

PARSER = "html.parser"

class Checker:
    def __init__(self, response):
        self.response = response
    
    def is_forbidden(self) -> bool:
        return self.response.status_code == 403    
        
    def search_results_is_empty(self) -> bool:
        soup = BeautifulSoup(self.response.text, PARSER)
        div = soup.find('div', class_='resultC2')
        
        if div:
            children = div.find_all(recursive=False)
            if len(children) == 2 and children[0].name == 'link' and children[1].name == 'h1':
                return False
            
    def page_is_empty(self) -> bool:
        return self.response.text.strip() == '<p class=maxLoad>Hela sökresultatet visas nu</p>'