import requests
import requests_cache

class Universalis():
    def __init__(self, cache_location="cache/universalis_cache", cache_expire_after=86400):
        """
        Initialize the universalis class.
        """
        self.apiBase = "https://universalis.app"

        self.cache_location = cache_location
        self.cache_expire_after = cache_expire_after
        self.session = requests_cache.CachedSession(
            cache_location, backend='sqlite', expire_after=cache_expire_after)
        
    def _do (self, endpoint, ep_params = None):
        full_query = self.apiBase + endpoint
        result = requests.get(full_query, params = ep_params)
        if 299 >= result.status_code >= 200:
            return result.json()
        elif result.status_code == 404:
            pass
        else:
            raise Exception(f'Error when requesting Universalis API:\n\
                            ({result.url}): [{result.status_code}] {result.reason}\n\
                            try later and check API status')
    def _do_cached (self, endpoint, ep_params = None):
        full_query = self.apiBase + endpoint
        result = self.session.get(full_query, params = ep_params)
        if 299 >= result.status_code >= 200:
            return result.json()
        elif result.status_code == 404:
            pass
        else:
            raise Exception(f'Error when requesting Universalis API:\n\
                            ({result.url}): [{result.status_code}] {result.reason}\n\
                            try later and check API status')
                            
    def data_centers(self):
        endpoint = "/api/v2/data-centers"
        return self._do_cached(endpoint)
    
    def worlds(self):
        endpoint = "/api/v2/worlds"
        return self._do_cached(endpoint)
    
    def market_board(self, worldDcRegion, itemIds, ep_params):
        endpoint = f"/api/v2/{worldDcRegion}/{itemIds}"
        return self._do(endpoint = endpoint, ep_params = ep_params)
    
    #rest to be added
