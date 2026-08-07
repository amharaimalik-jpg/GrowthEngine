import streamlit as st
from supabase import create_client
import stripe

# إعداد الصفحة
st.set_page_config(page_title="Growth Engine", page_icon="🚀", layout="wide")

# التحقق من الأسرار والاتصال
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("⚠️ يرجى التأكد من إدخال SUPABASE_URL و SUPABASE_KEY في إعدادات Secrets.")
    st.stop()

url = st.secrets["SUPABASE_URL"].strip()
key = st.secrets["SUPABASE_KEY"].strip()

if "STRIPE_API_KEY" in st.secrets:
    stripe.api_key = st.secrets["STRIPE_API_KEY"].strip()

try:
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")
    st.stop()

st.title("🚀 نظام إدارة الأعمال والمدفوعات الشامل")

# جلب البيانات مباشرة بدون تخزين مؤقت لضمان التحديث الفوري
try:
    res = supabase.table("sales").select("*").execute()
    sales_data = res.data if res else []
except Exception as e:
    sales_data = []

# تصميم التبويبات
tab1, tab2, tab3 = st.tabs(["💳 اللوحة المالية والصفقات", "👥 إدارة العملاء", "🤖 المساعد الذكي"])

with tab1:
    st.subheader("📊 لوحة الأرباح والمالية الحقيقية")
    
    # حساب إجمالي الأرباح من عمود amount
    total_sales = 0
    for item in sales_data:
        val = item.get('amount')
        if val is not None:
            try:
                total_sales += float(val)
            except:
                pass
                
    total_deals = len(sales_data)

    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الصفقات", f"{total_deals} صفقة")
    c2.metric("إجمالي الأرباح", f"${total_sales:,.2f} USD")
    c3.metric("سعر الخدمة القياسي", "$2,000.00 USD")

    st.write("---")
    st.subheader("📁 جدول البيانات الحي المباشر من Supabase")
    if sales_data:
        st.dataframe(sales_data, use_container_width=True)
    else:
        st.info("لا توجد بيانات ظاهرة في الجدول.")

with tab2:
    st.subheader("👥 العملاء والصفقات")
    if sales_data:
        for item in sales_data:
            c_name = item.get('client_name', 'عميل غير مسجل')
            c_amt = item.get('amount', 2000)
            c_status = str(item.get('status', '')).lower()
            
            if c_status == 'paid':
                st.success(f"✅ العميل: **{c_name}** | تمت الصفقة بنجاح بقيمة: ${float(c_amt):,.2f}")
            else:
                st.warning(f"🔄 العميل: **{c_name}** | قيد التفاوض بقيمة: ${float(c_amt):,.2f}")
    else:
        st.write("لا يوجد عملاء مسجلون حالياً.")

with tab3:
    st.subheader("🤖 المساعد الذكي للرد على استفسارات العملاء")
    user_query = st.text_input("اكتب سؤال العميل هنا (مثلاً: ما هي تكلفة الخدمة؟):")
    if user_query:
        if "سعر" in user_query or "تكلفة" in user_query or "كم" in user_query:
            st.info("💡 رد المساعد: تكلفة الخدمة الشاملة والنظام المتكامل هي 2,000 دولار أمريكي.")
        else:
            st.info("💡 رد المساعد: نحن نقدم نظاماً متكاملاً لإدارة الأعمال والمدفوعات بقيمة 2,000 دولار مع متابعة تامة للعملاء.")
