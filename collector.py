import requests
import time

def fetch_site_data(url):
    """إرسال الريكويست وجلب البيانات الخام من الخادم"""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GrowthEngine/2.0'
    }
    
    start_time = time.time()
    response = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
    latency = round(time.time() - start_time, 2)
    
    return {
        "final_url": response.url,
        "status_code": response.status_code,
        "headers": response.headers,
        "latency": latency
    }
