import time
import sqlite3
import threading
import requests
import streamlit as st
import stripe
from openai import OpenAI

# إعدادات العميل (المفتاح من الـ Secrets)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# ... (باقي كود قاعدة البيانات والبحث كما هو في السابق) ...

# 6. تحديث واجهة المستخدم لدمج وكيل المبيعات الذكي (tab2)
with tab2:
    st.subheader("💬 وكيل المبيعات الذكي (AI Negotiator)")
    
    # اختيار شركة للبدء معها
    company_options = [row['client_name'] for row in data]
    selected_company = st.selectbox("اختر شركة للتفاوض معها:", company_options)
    
    # إدارة حالة المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # إدخال المستخدم
    if prompt := st.chat_input("ماذا تريد أن تقول لهذا العميل؟ أو اطلب من الوكيل صياغة عرض"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # استدعاء العقل المدبر (AI)
        with st.chat_message("assistant"):
            # سياق المحادثة: إقناع العميل بخدماتنا
            system_prompt = f"""أنت وكيل مبيعات محترف. العميل المستهدف هو: {selected_company}.
            خدمتنا هي 'Autonomous Growth System' بقيمة 2000 دولار.
            مهمتك: التفاوض بذكاء، الإجابة على الاعتراضات، وإقناع العميل بالقيمة.
            كن مقنعاً، واحترافياً، ومختصراً."""
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            ai_response = response.choices[0].message.content
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
