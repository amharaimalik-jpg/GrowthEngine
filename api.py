import streamlit as st
import google.generativeai as genai

def get_ai_closer_response(customer_input, history_str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # البحث التلقائي عن أي نموذج مدعوم في حسابك لمنع أخطاء 404 نهائياً
        target_model = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                target_model = m.name
                break
        
        if not target_model:
            target_model = 'gemini-1.5-flash'
            
        model = genai.GenerativeModel(target_model)
        
        system_instruction = "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
        
        full_prompt = f"{system_instruction}\n\nسجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"
