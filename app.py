import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Growth Engine - Live", layout="wide")

# الاتصال بقاعدة البيانات
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("⚡ نظام Growth Engine الحقيقي")

# جلب البيانات فقط من قاعدة البيانات
def get_live_data():
    return supabase.table("sales").select("*").execute().data

data = get_live_data()
total_revenue = sum(float(i['amount']) for i in data if i.get('status') == 'paid')

st.metric("الأرباح الحقيقية المحصلة", f"${total_revenue:,.2f}")
st.dataframe(data)
