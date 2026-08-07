import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    if "GEMINI_API_KEY" not in st.secrets:
        return "⚠️ خطأ: مفتاح GEMINI_API_KEY غير موجود في إعدادات Streamlit Secrets."
        
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # قائمة النماذج المعتمدة والمستقرة فقط بدون أي جلب عشوائي
    models_to_try = ["gemini-1.5-flash", "gemini-pro"]
    
    prompt = f"""أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار.
قواعد الرد الإلزامية:
1. أجب بدقة وعمق حصرياً على السؤال أو الاعتراض الحالي الذي طرحه العميل (مثل السعر، الضمان، إلخ) دون أي تكرار لردود سابقة.
2. ادمج بذكاء شرح استراتيجيات جلب العملاء المستهدفين وزيادة حركة المرور (Traffic & Outreach - المهمة رقم 3) وكيف يقوم محرك النظام باستقطاب العملاء المستهدفين بدقة عالية لعملك.
3. كن مقنعاً، احترافياً، ووجه العميل نحو رابط التحويل والتفعيل بمهارة لإتمام الصفقة.

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
    
    last_error = ""
    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            req = urllib.request.Request(
                url, 
                data=data, 
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                if 'candidates' in res_json and len(res_json['candidates']) > 0:
                    parts = res_json['candidates'][0]['content']['parts']
                    if parts and 'text' in parts[0]:
                        return parts[0]['text']
        except Exception as e:
            last_error = str(e)
            continue
            
    return f"⚠️ خطأ تقني في الاتصال: {last_error}"
