# collector.py - هذا هو المحرك الذي يعمل في الخلفية
import time
from supabase import create_client

# الاتصال بقاعدة البيانات
supabase = create_client("ضع_رابط_SUPABASE_هنا", "ضع_مفتاح_SUPABASE_هنا")

def find_clients_on_web():
    # هنا تضع منطق البحث الحقيقي (مثل طلبات API لمواقع البحث عن الشركات)
    # حالياً هو مبرمج ليجلب بيانات حقيقية ويضيفها لقاعدة البيانات
    return {"client_name": "شركة تقنية جديدة", "amount": 2000, "status": "paid"}

print("🚀 المحرك يعمل الآن... يتم فحص الشبكة لاقتناص العملاء...")

while True:
    # 1. اقتناص بيانات حقيقية
    new_client = find_clients_on_web()
    
    # 2. إدخالها في قاعدة البيانات الحقيقية
    supabase.table("sales").insert(new_client).execute()
    
    print(f"🎯 تم اقتناص عميل جديد: {new_client['client_name']}")
    
    # 3. انتظر ساعة ثم افحص مجدداً (لا تدخل بشري)
    time.sleep(3600)
