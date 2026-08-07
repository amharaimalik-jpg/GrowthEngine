import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    try:
        # التحقق من وجود المفتاح في إعدادات الـ Secrets
        if "GEMINI_API_KEY" not in st.secrets:
            return "⚠️ خطأ: مفتاح GEMINI_API_KEY غير موجود في إعدادات Secrets في Streamlit."
            
        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        # دمج الشخصية، الإجابة المخصصة للسؤال، ودمج المهمة 3 (Traffic & Outreach)
        prompt = f"""أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار.
قواعد الرد الإلزامية:
1. أجب بدقة وعمق حصرياً على السؤال أو الاعتراض الحالي الذي طرحه العميل (مثل السعر، الضمان، إلخ) دون أي تكرار لردود سابقة.
2. ادمج بذكاء شرح استراتيجيات جلب العملاء المستهدفين وزيادة حركة المرور (Traffic & Outreach - المهمة رقم 3) وكيف يقوم محرك النظام باستقطاب العملاء بدقة عالية.
3. كن مقنعاً، احترافياً، ووجه العميل نحو رابط التحويل والتفعيل بمهارة.

سجل المحادثة السابق:
{history_str}

رسالة العميل الحالية:
{customer_input}"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=20) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                parts = res_json['candidates'][0]['content']['parts']
                if parts and 'text' in parts[0]:
                    return parts[0]['text']
                    
        return "⚠️ تنبيه: استجابة خادم جوجل وصلت فارغة."
                
    except Exception as e:
        # إظهار الخطأ التقني الحقيقي بوضوح تام لنعرف السبب جذرياً
        return f"⚠️ خطأ تقني صريح: {str(e)}"
