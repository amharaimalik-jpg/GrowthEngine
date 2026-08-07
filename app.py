import streamlit as st
from supabase import create_client

# تنظيف الروابط تلقائياً من أي مسافات مخفية لمنع خطأ الاتصال
SUPABASE_URL = st.secrets["SUPABASE_URL"].strip()
SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()

# الاتصال بقاعدة البيانات
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_real_sales_data():
    try:
        response = supabase.table("sales").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return []

tab1, tab2, tab3 = st.tabs(["الرئيسية", "العملاء", "المالية"])

with tab3:
    st.subheader("💳 لوحة المالية الحقيقية")
    
    sales_data = get_real_sales_data()
    
    if sales_data:
        total_sales = sum(float(item.get('amount', 0)) for item in sales_data)
        total_deals = len(sales_data)
    else:
        total_sales = 0
        total_deals = 0
    
    col1, col2 = st.columns(2)
    col1.metric("إجمالي الصفقات المغلقة", f"{total_deals} صفقة")
    col2.metric("إجمالي الأرباح المحصلة", f"${total_sales:,.2f} USD")
    
    st.write("---")
    st.write("البيانات يتم تحديثها مباشرة من قاعدة البيانات.")
