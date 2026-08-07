import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    # قائمة النماذج لتجربتها تلقائياً ومنع أي خطأ 404 نهائياً
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        return "عذراً، مفتاح الـ API غير موجود في ملف الـ Secrets."
        
    system_instruction = "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
    
    prompt = f"{system_instruction}\n\nسجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
    
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
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                if 'candidates' in res_json and len(res_json['candidates']) > 0:
                    return res_json['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            last_error = str(e)
            continue
            
    return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي تأكد من صحة المفتاح. التفاصيل: {last_error}"
