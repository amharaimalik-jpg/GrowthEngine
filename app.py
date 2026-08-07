import streamlit as st
from supabase import create_client
import re

# قراءة البيانات وتنظيفها تماماً من أي مسافات، علامات تنصيص، أو رموز مخفية
raw_url = str(st.secrets.get("SUPABASE_URL", ""))
raw_key = str(st.secrets.get("SUPABASE_KEY", ""))

url = re.sub(r'[\s"\'`]', '', raw_url)
key = re.sub(r'[\s"\'`]', '', raw_key)

st.write(f"🔍 الرابط بعد التنظيف: `{url}`")

try:
    supabase = create_client(url, key)
    response = supabase.table("sales").select("*").execute()
    st.success("تم الاتصال بقاعدة البيانات بنجاح!")
except Exception as e:
    st.error(f"خطأ الاتصال التفصيلي: {e}")

tab1, tab2, tab3 = st.tabs(["الرئيسية", "العملاء", "المالية"])

with tab3:
    st.subheader("💳 لوحة المالية الحقيقية")
    sales_data = []
    try:
        res = supabase.table("sales").select("*").execute()
        sales_data = res.data
    except:
        pass
    
    total_sales = sum(float(item.get('amount', 0)) for item in sales_data) if sales_data else 0
    total_deals = len(sales_data) if sales_data else 0
    
    col1, col2 = st.columns(2)
    col1.metric("إجمالي الصفقات المغلقة", f"{total_deals} صفقة")
    col2.metric("إجمالي الأرباح المحصلة", f"${total_sales:,.2f} USD")
