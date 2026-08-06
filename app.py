import streamlit as st
import db_manager
import offer_config
import scraper
import outreach
import payment_gateway
import pandas as pd
from api import get_ai_closer_response

st.set_page_config(page_title="GrowthEngine Web Dashboard", page_icon="🚀", layout="wide")

st.title("🚀 GrowthEngine Master Control Center - Web Dashboard")
st.markdown(f"### 💡 Active Offer: `{offer_config.OFFER_TITLE}` | Price: **${offer_config.OFFER_PRICE} USD**")

# تقسيم الشاشة إلى عمودين: لوحة التحكم يمين/يسار، وشات المبيعات بجانبها
tab1, tab2 = st.tabs(["📊 لوحة البيانات والتحكم", "💬 وكيل المبيعات الذكي (AI Closer)"])

with tab1:
    st.subheader("📋 Live SQLite Database Records")
    try:
        conn = db_manager.get_connection()
        df = pd.read_sql("SELECT * FROM leads", conn)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.info("لا توجد بيانات مسجلة في قاعدة البيانات حتى الآن.")

with tab2:
    st.subheader("💬 محادثة وكيل الإغلاق الفوري")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if customer_input := st.chat_input("اكتب رسالة العميل هنا لاختبار وكيل الإغلاق..."):
        st.session_state.messages.append({"role": "user", "content": customer_input})
        with st.chat_message("user"):
            st.markdown(customer_input)

        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        
        with st.chat_message("assistant"):
            with st.spinner("جاري صياغة رد الإغلاق بقوة..."):
                ai_reply = get_ai_closer_response(customer_input, history_str)
                st.markdown(ai_reply)
                
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
