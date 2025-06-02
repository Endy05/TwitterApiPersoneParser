from config import data

class RateLimiter:
    def __init__(self):
        self.list_change_data = data['request_data']['profile']['list_changeData']


    def get_data_keys(self):
        return self.list_change_data.keys()
        
    def get_data_for_key(self, key):
        return self.list_change_data.get(key)
    
    def get_rate_limit(self):
        len_data_keys = len(self.get_data_keys())
        rate_limit_tweet = 18 / len_data_keys
        rate_limit_profile = 6 / len_data_keys
        return rate_limit_tweet, rate_limit_profile
