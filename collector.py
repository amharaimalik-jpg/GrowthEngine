import time
import requests
from supabase import create_client

# 1. إعدادات قاعدة بيانات Supabase
SUPABASE_URL = "ضع_رابط_SUPABASE_هنا"
SUPABASE_KEY = "ضع_مفتاح_SUPABASE_هنا"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. إعدادات Google Custom Search API (للبحث الحقيقي في الويب)
GOOGLE_API_KEY = "مفتاح_جوجل_API_الخاص_بك"
SEARCH_ENGINE_ID = "معرف_محرك_البحث_المخصص_CSE_ID"

def fetch_real_companies_from_web():
    try:
        # الكلمات المفتاحية للبحث عن الشركات والعملاء المستهدفين في الإنترنت
        query = "software development company startups digital agency"
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        
        response = requests.get(url)
        data = response.json()
        
        if "items" in data:
            for item in data["items"]:
                company_name = item.get("title", "شركة رقمية")
                
                # التحقق مما إذا كانت الشركة مسجلة مسبقاً لمنع التكرار
                existing = supabase.table("sales").select("*").eq("client_name", company_name).execute()
                if not existing.data:
                    client_data = {
                        "client_name": company_name,
                        "amount": 2000,
                        "status": "lead" # قيد التفاوض والاقتناص
                    }
                    supabase.table("sales").insert(client_data).execute()
                    print(f"🎯 تم اقتناص شركة حقيقية من الويب وإضافتها: {company_name}")
                    return
        print("⏳ جاري مسح الويب والبحث عن شركات جديدة...")
    except Exception as e:
        print(f"⚠️ خطأ أثناء البحث في الشبكة: {e}")

print("🚀 المحرك الذكي الحقيقي للبحث في الويب يعمل الآن 24/7...")

while True:
    fetch_real_companies_from_web()
    # الانتظار لمدة ساعة (3600 ثانية) قبل عملية البحث والمسح التالية لتجنب استنفاد حدود الـ API
    time.sleep(3600)
