class Search:
    def __init__(self, gender=None, min=None, max=None, geo=None, name="", pid="", phone="", id=""):
        self.gender = gender
        self.min = min
        self.max = max
        self.geo = geo

        self.name = name
        self.phone = phone
        self.pid = pid
        self.id = id

        self.search = name if name else phone if phone else pid if pid else id if id else None
    
    def get_user_url(self):
        return f"https://mrkoll.se/resultat?n={self.search.replace(' ', '+')}"
    
    def get_main_url(self):
        return f"https://mrkoll.se/resultat?n={self.search.replace(' ', '+')}&c={self.geo}&min={self.min}&max={self.max}&sex={self.gender}&c_stat=all&company="