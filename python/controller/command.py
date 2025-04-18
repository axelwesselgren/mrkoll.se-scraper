from model.model import Model
from view.console import print_info, print_success, print_warning
from scraper import search_profiles, load_next_page, load_profile
from data.search import Search
from enums.change import Change
import requests

class Command():
    def __init__(self, model: Model):
        self.model = model
        self.model.add_property_change_listener(self.listener)
    
    def execute(self):
        if not self.model.command: return
        command, flags = self.model.command
        match command:
            case "help":
                self.model.fire_property_change(Change.HELP)
                # prompt_and_check(valid_command, execute_command)
                return self.model.prompt_and_check()
            case "show":
                self.model.fire_property_change(Change.SHOW)
                if not self.model.results_preview:
                    print_warning("Nothing searched")
                return self.model.prompt_and_check()
            case "search":
                session = requests.Session()
                current_page = 1
                search = Search(flags['gender'], flags['min'], flags['max'], flags['geo'], name=flags['name'], pid=flags['pid'])
                results_now = search_profiles(search, session, self.model.debug)
                if not results_now:
                    return self.model.prompt_and_check()
                print_success(f"Found {len(results_now)} people")
                self.model.results_preview = results_now
                return self.model.prompt_and_check()
            case "next":
                self.model.current_page += 1
                page = load_next_page(session, self.model.current_page, 0)
                if not page:
                    print_warning(f"Failed loading index [{self.model.current_page}]")
                    self.model.current_page -= 1 
                    return
                self.model.results_preview.extend(page)
                print_success(f"Indexed page [{self.model.current_page}]")
                return self.model.prompt_and_check()
            case "lookup":
                if not flags['phone'] and not flags['pid']:
                    for user in self.model.results:
                        if self.model.results_preview[flags['index']].id == user.id:
                            print_info("User already looked up")
                            # display user
                            return self.model.prompt_and_check()
                
                    user = load_profile(Search(id=self.model.results_preview[flags['index']].id))
                    if not user:
                        print_warning("Unable to look up user") 
                        return self.model.prompt_and_check()
                    self.model.results.append(user)
                    print_info(f"Looked up [{user.pid}]")

                if flags['phone']:
                    for user in self.model.results:
                        if flags['phone'] in user.phone_number:
                            print_warning("User already looked up")
                            #display user
                            return self.model.prompt_and_check()
                        
                    user = load_profile(Search(phone=flags['phone']))
                    if not user:
                        print_warning("Unable to look up user")
                        return
                    self.model.results.append(user)
                    print_info(f"Looked up [{user.pid}]")

                if flags['pid']:
                    for user in self.model.results:
                        if flags['pid'] == user.pid:
                            print_warning("Person already looked up")
                            #display user
                            return
                        
                    user = load_profile(Search(pid=flags['pid']))
                    if not user:
                        print_warning("Unable to look up user")
                        return
                    self.model.results.append(user)
                    print_info(f"Looked up [{user.pid}]")
                return
            case _:
                print_warning("DEBUG ERROR")
                return
            
    def listener(self, value, old, new):
        match value:
            case "EXECUTE":
                self.execute()
                return
            case _:
                return