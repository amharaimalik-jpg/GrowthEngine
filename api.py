import streamlit as st
import google.generativeai as genai

def get_ai_closer_response(customer_input, history_str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # قائمة النماذج لتجربتها بالترتيب حتى يعمل النموذج المتاح لديك
        models_to_try = ['gemini-2.0-flash-lite', 'gemini-1.5-flash', 'gemini-2.0-flash']
        
        system_instruction = "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
        full_prompt = f"{system_instruction}\n\nسجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                if response and response.text:
                    return response.text
            except Exception as ex:
                last_error = str(ex)
                continue
                
        return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {last_error}"
    except Exception as e:
        return f"عذراً، حدث خطأ عام: {str(e)}"
