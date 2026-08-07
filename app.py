import streamlit as st
from supabase import create_client

# قراءة القيم وعرضها للتأكد منها
url = st.secrets.get("SUPABASE_URL", "غير موجود")
key = st.secrets.get("SUPABASE_KEY", "غير موجود")

st.write(f"📍 الرابط المقروء حالياً: `{url}`")
st.write(f"🔑 طول المفتاح المقروء: `{len(key)}` حرف")

try:
    supabase = create_client(url.strip(), key.strip())
    response = supabase.table("sales").select("*").execute()
    st.success("تم الاتصال بنجاح!")
    st.write(response.data)
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
