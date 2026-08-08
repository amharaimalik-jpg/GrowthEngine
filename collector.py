import time
import requests

class RobustGoogleSearch:
    def __init__(self, api_keys, search_engine_id):
        """
        يقبل مفتاحاً مفرداً (نص) أو قائمة مفاتيح لضمان التبديل التلقائي عند النفاد.
        """
        if isinstance(api_keys, str):
            self.api_keys = [api_keys]
        else:
            self.api_keys = api_keys
        self.cx = search_engine_id
        self.current_key_index = 0

    def get_current_key(self):
        if not self.api_keys:
            return ""
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            print(f"تم تبديل مفتاح جوجل تلقائياً إلى الفهرس: {self.current_key_index}")

    def search(self, query, num_results=10, retries=3):
        url = "https://www.googleapis.com/customsearch/v1"
        for attempt in range(retries):
            api_key = self.get_current_key()
            if not api_key:
                print("تحذير: لا يوجد مفتاح API متاح.")
                break
                
            params = {
                'key': api_key, 
                'cx': self.cx, 
                'q': query, 
                'num': min(num_results, 10)
            }
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    return response.json().get('items', [])
                elif response.status_code in [403, 429]: 
                    print(f"انتهى حد الاستخدام للمفتاح الحالي (رمز: {response.status_code}). جاري التبديل...")
                    self.rotate_key()
                else:
                    print(f"خطأ في الاتصال برمز: {response.status_code}")
                    time.sleep(2)
            except Exception as e:
                wait_time = 2 ** attempt
                print(f"خطأ في الشبكة، إعادة المحاولة خلال {wait_time} ثوانٍ...")
                time.sleep(wait_time)
        return []

def get_leads_from_google(query, api_keys, search_engine_id, num_results=10):
    """
    الدالة الرئيسية الموحدة لاستدعاء البحث بذكاء وأمان تام داخل مشروعك.
    """
    bot = RobustGoogleSearch(api_keys, search_engine_id)
    return bot.search(query, num_results=num_results)
