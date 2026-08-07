import streamlit as st
import google.generativeai as genai

def get_ai_closer_response(customer_input, history_str):
    try:
        # استدعاء مفتاح السري من إعدادات ستريمليت
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # إعداد شخصية وكيل المبيعات
        system_instruction = (
            "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم "
            "(AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. "
            "هدفك الرد باحترافية، الإجابة عن أسئلة العميل بدقة، وإقناعه بإغلاق الصفقة."
        )
        
        # تهيئة النموذج مع التعليمات المباشرة
        generation_config = {"temperature": 0.7}
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction,
            generation_config=generation_config
        )
        
        # دمج سجل المحادثة مع رسالة العميل الحالية
        prompt = f"سجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"
