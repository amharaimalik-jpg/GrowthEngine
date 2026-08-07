import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        # استخدام الإصدار المستقر v1 لضمان عمل نموذج gemini-1.5-flash بدون أخطاء
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = (
            "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم "
            "(AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. "
            "هدفك الأساسي هو الرد باحترافية كاملة، الإجابة بدقة وحسب السؤال أو الاستفسار "
            "الذي يطرحه العميل في رسالته الحالية، وإقناعه بإغلاق الصفقة."
        )
        
        full_prompt = (
            f"{system_instruction}\n\n"
            f"سجل المحادثة السابق:\n{history_str}\n\n"
            f"رسالة العميل الحالية: {customer_input}"
        )
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }]
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                return res_json['candidates'][0]['content']['parts'][0]['text']
                
    except Exception as e:
        return f"⚠️ حدث خطأ في الاتصال: {str(e)}"
        
    return "عذراً، لم يتم استلام رد."
