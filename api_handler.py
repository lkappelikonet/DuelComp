import requests

# Skeleton class for now, no real reason to do anything with this at the moment

class ApiHandler_YGOrgDB:

    api_root = r"https://db.ygorganization.com/"
    config_path = r""

    def __init__(self): # TODO load cache from config file
        self.cache = {}

    def __del__(self): # TODO write cache to config file
        pass

    #def create_request(self, url, params=[], headers=[]):
    #    apireturn = create_request(r"https://db.ygorganization.com/data/card/15110")
    #    print(apireturn.json()["cardData"]["en"]["name"])
    #    try:
    #        return requests.get(url, params=params, headers=headers)
    #    except BaseException:
    #        print(BaseException)
    #    return None



