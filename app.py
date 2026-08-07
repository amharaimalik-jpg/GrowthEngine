# app.py
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Growth Engine Dashboard", layout="wide")

# الاتصال
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("💰 لوحة الأرباح والعملاء الحقيقيين")

# جلب البيانات
res = supabase.table("sales").select("*").execute()
data = res.data

# عرض الأرباح
total_revenue = sum(float(i['amount']) for i in data if i['status'] == 'paid')
total_leads = len(data)

col1, col2 = st.columns(2)
col1.metric("إجمالي العملاء المقتنصين", total_leads)
col2.metric("الأرباح المحصلة ($)", total_revenue)

st.dataframe(data)
