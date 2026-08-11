import requests
import time
import re

def clean_url(url):
    """تنظيف الرابط وإزالة الأقواس والمسافات وعلامات التنصيص الزائدة"""
    # إزالة المسافات والأقواس الزائدة
    url = url.strip().strip("()[]\"'")
    
    # تأكيد وجود البروتوكول الصحيح
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    return url

def fetch_site_data(url):
    """إرسال الريكويست وجلب البيانات الخام بعد تنظيف الرابط"""
    clean_target_url = clean_url(url)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GrowthEngine/2.0'
    }
    
    start_time = time.time()
    response = requests.get(clean_target_url, headers=headers, timeout=12, allow_redirects=True)
    latency = round(time.time() - start_time, 2)
    
    return {
        "final_url": response.url,
        "status_code": response.status_code,
        "headers": response.headers,
        "latency": latency
    }
