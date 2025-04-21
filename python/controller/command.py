from model.model import Model
from view.logger import Logger
from scraper.scraper import Scraper
from data.search import Search
from enums.change import Change

class Command():
    def __init__(self, model: Model):
        self.model = model
        self.model.add_property_change_listener(self.listener)
    
    def execute(self):
        if not self.model.command: 
            return
        
        command, flags = self.model.command
        
        match command:
            case "help":
                self.model.fire_property_change(Change.HELP)
            case "show":
                self.model.fire_property_change(Change.SHOW)
                if not self.model.results_preview:
                    Logger.warning("Nothing searched")
            case "search":
                self.search(flags)
            case "next":
                self.next()
            case "lookup":
                user = self.model.load_profile()
                if not user:
                    Logger.warning("Unable to look up user")
                    return
                
                self.model.results.append(user)
                Logger.info(f"Looked up [{user.pid}]")
            case _:
                Logger.warning("DEBUG ERROR")
                return
            
        return self.model.prompt_and_check()
    
    def search(self, flags):
        search = Search(
            flags['gender'], 
            flags['min'], 
            flags['max'], 
            flags['geo'], 
            name=flags['name'],
            pid=flags['pid']
        )
        
        self.model.search = search
        
        scraper = Scraper(self.model)
        results_now = scraper.search_profiles()
        
        if not results_now:
            return self.model.prompt_and_check()
        
        Logger.success(f"Found {len(results_now)} people")
        self.model.results_preview = results_now
        
    def next(self):
        self.model.current_page += 1
        scraper = Scraper(self.model)
        page = scraper.load_next_page()
        
        if not page:
            Logger.warning(f"Failed loading index [{self.model.current_page}]")
            self.model.current_page -= 1
            return
        
        self.model.results_preview.extend(page)
        Logger.success(f"Indexed page [{self.model.current_page}]")
        
    def listener(self, value, old, new):
        match value:
            case "EXECUTE":
                self.execute()
                return
            case _:
                return