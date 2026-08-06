import streamlit as st
import google.generativeai as genai

def get_ai_closer_response(customer_input, history_str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # استخدام النموذج المستقر مع النسخة المحدثة
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_instruction = "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
        
        full_prompt = f"{system_instruction}\n\nسجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"
