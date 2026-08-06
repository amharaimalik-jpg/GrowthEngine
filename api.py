import os
import streamlit as st
from openai import OpenAI

# تعيين المفتاح من أسرار ستريمليت إلى بيئة النظام ليقرأه عميل أوبن إيه آي تلقائياً
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

def get_ai_closer_response(customer_input, history_str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
                },
                {
                    "role": "user", 
                    "content": f"سجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
                }
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"
