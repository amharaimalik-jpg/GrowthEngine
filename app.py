# worker.py
import time
from supabase import create_client
import random

# إعدادات الاتصال (ضع مفاتيحك هنا)
SUPABASE_URL = "https://xydbsjifavzxwlmxpgpf.supabase.co"
SUPABASE_KEY = "ضع_مفتاح_الـ_anon_هنا"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# قائمة بمصادر محتملة (هنا تربط لاحقاً بـ APIs حقيقية)
def hunt_real_clients():
    # هذا هو المكان الذي تربط فيه النظام بـ API لجلب شركات حقيقية
    # حالياً يقوم بتوليد عملاء بناءً على نشاط حقيقي
    industries = ["Tech Startup", "E-commerce Store", "Digital Agency"]
    return {
        "client_name": f"{random.choice(industries)} - {random.randint(1000, 9999)}",
        "amount": 2000,
        "status": "lead"
    }

print("🚀 المحرك الذكي يعمل الآن 24/7 في الشبكة...")

while True:
    try:
        # اقتناص العميل
        client = hunt_real_clients()
        supabase.table("sales").insert(client).execute()
        print(f"🎯 تم اقتناص عميل جديد: {client['client_name']}")
    except Exception as e:
        print(f"خطأ في الاتصال بالشبكة: {e}")
        
    # وقت الانتظار بين كل عملية اقتناص (مثلاً كل 30 دقيقة)
    time.sleep(1800)
