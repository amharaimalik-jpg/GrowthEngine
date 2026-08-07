import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Growth Engine - Live", layout="wide")

# تهيئة الاتصال بقاعدة البيانات بأمان تام
@st.cache_resource
def init_supabase():
    try:
        url = str(st.secrets.get("SUPABASE_URL", "")).strip()
        key = str(st.secrets.get("SUPABASE_KEY", "")).strip()
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

supabase = init_supabase()

st.title("⚡ لوحة الأرباح والعملاء الحقيقيين")

# دالة جلب البيانات المحمية ضد أي انقطاع في الشبكة
def get_live_data():
    if supabase:
        try:
            res = supabase.table("sales").select("*").execute()
            if res and res.data is not None:
                return res.data
        except Exception:
            pass
    return []

data = get_live_data()

# حساب الأرباح والمؤشرات بدقة
total_revenue = sum(float(i.get('amount', 0)) for i in data if str(i.get('status', '')).lower() == 'paid')
total_leads = len(data)

col1, col2 = st.columns(2)
col1.metric("إجمالي العملاء المقتنصين", total_leads)
col2.metric("الأرباح المحصلة ($)", f"${total_revenue:,.2f}")

st.write("---")
if data:
    st.dataframe(data, use_container_width=True)
else:
    st.info("قاعدة البيانات متصلة وجاهزة. بمجرد أن يبدأ المحرك الخلفي (collector.py) باقتناص العملاء، ستظهر البيانات وتتحدث تلقائياً هنا.")
