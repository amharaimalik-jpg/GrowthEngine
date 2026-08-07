import streamlit as st
from supabase import create_client

# 1. الاتصال بقاعدة البيانات
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def get_real_sales_data():
    try:
        response = supabase.table("sales").select("*").execute()
        return response.data
    except Exception as e:
        return []

# 2. تعريف التبويبات (تأكد من وجود هذا السطر قبل استخدام tab3)
tab1, tab2, tab3 = st.tabs(["الرئيسية", "العملاء", "المالية"])

# 3. عرض البيانات داخل التبويب الثالث
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
