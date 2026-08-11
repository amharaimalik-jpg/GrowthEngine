import time
import smtp_service # أو استخدام مكتبة البريد التلقائي
from collector import fetch_site_data
from engine import analyze_performance

# قائمة النطاقات أو المتاجر المستهدفة للفحص الآلي في الخلفية
TARGET_STORES = [
    "https://www.gymshark.com",
    "https://www.allbirds.com",
    "https://www.woocommerce.com"
]

def run_background_traffic_bot():
    """محرك الجلب الآلي: يفحص المتاجر ويرسل تقارير فورية لأصحابها"""
    print("[*] Starting Background Autonomous Outreach Engine...")
    
    for store_url in TARGET_STORES:
        try:
            # 1. فحص المتجر تلقائياً
            raw_data = fetch_site_data(store_url)
            audit_result = analyze_performance(raw_data)
            
            # 2. تقييم ما إذا كان المتجر يحتاج تحسين
            if audit_result["score"] < 90 or raw_data["latency"] > 0.8:
                print(f"[!] Target Found: {store_url} | Score: {audit_result['score']} | Latency: {raw_data['latency']}s")
                
                # 3. إنشـاء رابط التقرير المباشر المخصص للمتجر
                report_link = f"https://growthengine-9btijzf8jcjty9hfqufsbu.streamlit.app/?target={store_url}"
                
                # 4. طباعة الرسالة التلقائية المجهزة للإرسال الآلي
                print(f"[➔] Automated Pitch Generated for {store_url}:")
                print(f"    'Hello, we detected a {raw_data['latency']}s response delay on your server. View live patch: {report_link}'")
                
        except Exception as e:
            print(f"[-] Error auditing {store_url}: {e}")
            
        time.sleep(2) # فاصل زمني لتجنب حظر السيرفر

if __name__ == "__main__":
    run_background_traffic_bot()
