import requests_cache

class GarlandTools():
    def __init__(self, cache_location="cache/garlandtools_cache", cache_expire_after=86400, language="en"):
        """
        Initialize the GarlandTools class.
        """
        if language in ["en", "ja", "fr", "de"]:
            self.language = language
        else:
            raise Exception("GarlantTools API Language not valid, it must be \"en\", \"ja\", \"fr\", or \"de\"")
        self.apiBase = "https://garlandtools.org/api"

        self.cache_location = cache_location
        self.cache_expire_after = cache_expire_after
        self.session = requests_cache.CachedSession(
            cache_location, backend='sqlite', expire_after=cache_expire_after)
        
    def _do_cached (self, endpoint = "/get.php", ep_params = None):
        full_query = self.apiBase + endpoint
        result = self.session.get(full_query, params = ep_params)
        if 299 >= result.status_code >= 200:
            return result.json()
        else:
            raise Exception(f'Error when requesting GarlantTools API:\n\
                            ({result.url}): [{result.status_code}] {result.reason}\n\
                            try later and check API status')
        
    def core(self):
        ep_params = {'id':'data', 'type':'core','lang':self.language, 'version':3}
        return self._do_cached(ep_params = ep_params)
    
    def browse(self, catagory):
        catagories = ["achievement", "action", "fate", "fishing", "item", "leve", "mob", "node", "npc", "quest", "status"]
        if catagory not in catagories:
            raise Exception(f'provide catagory not available, please check again')
        ep_params = {'id':catagory, 'type':'browse', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def achievement(self, id):
        ep_params = {'id':id, 'type':'achievement', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def action(self, id):
        ep_params = {'id':id, 'type':'action', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def fate(self, id):
        ep_params = {'id':id, 'type':'fate', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def fishing(self, id):
        ep_params = {'id':id, 'type':'fishing', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def item(self, id):
        ep_params = {'id':id, 'type':'item', 'lang':self.language, 'version':3}
        return self._do_cached(ep_params = ep_params)
        
    def leve(self, id):
        ep_params = {'id':id, 'type':'leve', 'lang':self.language, 'version':3}
        return self._do_cached(ep_params = ep_params)
        
    def mob(self, id):
        ep_params = {'id':id, 'type':'mob', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def node(self, id):
        ep_params = {'id':id, 'type':'node', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def npc(self, id):
        ep_params = {'id':id, 'type':'npc', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def quest(self, id):
        ep_params = {'id':id, 'type':'quest', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
    def status(self, id):
        ep_params = {'id':id, 'type':'status', 'lang':self.language, 'version':2}
        return self._do_cached(ep_params = ep_params)
        
# Module to add:
    # Map 
    # Venture
    # Icon
    # Search
