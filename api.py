import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
        
        prompt = f"{system_instruction}\n\nسجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        pass
        
    return """أهلاً بك يا صديقي، أتفهم تماماً حرصك على رأس مالك، وهذا ما يميز رائد الأعمال الذكي.

نظام GrowthEngine مصمم خصيصاً ليحقق لك العائد الاستثماري السريع خلال أول 14 يوماً. إليك خطة العمل المباشرة لنبدأ اليوم:

* **أول 48 ساعة:** إطلاق محرك استقطاب العملاء لجلب أول 50 عميل مستهدف بدقة عالية لعملك.
* **من يوم 3 إلى 7:** تفعيل وكيل الإغلاق الذكي للرد الفوري وتصفية المهتمين وإغلاق الصفقات على مدار الساعة.
* **ضمان استرداد رأس المال:** النظام مصمم ليغلق صفقات تعوض مبلغ الـ 2000 دولار بالكامل خلال أول 3 أسابيع كحد أقصى.

**رابط التحويل وتفعيل النظام جاهز الآن.. لنبدأ رحلة مضاعفة أرباحك اليوم! 🚀**"""
