import time
import requests

class RobustGoogleSearch:
    def __init__(self, api_keys, search_engine_id):
        self.api_keys = api_keys
        self.cx = search_engine_id
        self.current_key_index = 0

    def get_current_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

    def search(self, query, num_results=10, retries=3):
        url = "https://www.googleapis.com/customsearch/v1"
        for attempt in range(retries):
            api_key = self.get_current_key()
            params = {'key': api_key, 'cx': self.cx, 'q': query, 'num': min(num_results, 10)}
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    return response.json().get('items', [])
                elif response.status_code in [403, 429]: 
                    self.rotate_key()
                else:
                    time.sleep(2)
            except:
                time.sleep(2 ** attempt)
        return []
