import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # قائمة النماذج للتجربة التلقائية لضمان عدم حدوث خطأ 404 نهائياً
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.0-pro"
    ]
    
    # تعليمات النظام شاملة الإجابة المخصصة ودمج المهمة 3 (Traffic & Outreach)
    system_instruction = (
        "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم "
        "(AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار.\n"
        "قواعد الرد الصارمة:\n"
        "1. أجب بدقة واحترافية تامة حصرياً على السؤال أو الاعتراض الذي يطرحه العميل في رسالته الحالية.\n"
        "2. لا تكرر إجابات ثابتة أو محفوظة، بل خصص ردك بناءً على سياق سؤال العميل.\n"
        "3. ادمج شرح استراتيجيات جلب العملاء المستهدفين وزيادة حركة المرور (Traffic & Outreach - المهمة 3) وكيف يقوم محرك النظام باستهداف العملاء بدقة عالية.\n"
        "4. تعامل مع مخاوف السعر والضمان بحكمة، ووجه العميل نحو رابط التحويل والتفعيل بمهارة واحترافية."
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
    
    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                if 'candidates' in res_json and len(res_json['candidates']) > 0:
                    text_resp = res_json['candidates'][0]['content']['parts'][0]['text']
                    if text_resp:
                        return text_resp
        except Exception:
            continue
            
    return "أهلاً بك يا صديقي. بصفتي وكيل مبيعات GrowthEngine، أنا جاهز للإجابة عن أي استفسار يخص جلب العملاء وإغلاق الصفقات. تفضل بسؤالك!"
