import streamlit as st
from supabase import create_client
import stripe
import re

raw_url = str(st.secrets.get("SUPABASE_URL", ""))
raw_key = str(st.secrets.get("SUPABASE_KEY", ""))
url = re.sub(r'[\s"\'`]', '', raw_url)
key = re.sub(r'[\s"\'`]', '', raw_key)

supabase = create_client(url, key)
stripe.api.key = st.secrets.get("STRIPE_API_KEY", "")

tab1, tab2, tab3 = st.tabs(["الرئيسية", "العملاء", "المالية"])

with tab1:
    st.subheader("🚀 لوحة التحكم الرئيسية")
    st.write("مرحباً بك في نظام إدارة الأعمال والمدفوعات الخاص بك.")
    
    st.markdown("### 💳 اطلب خدمتك الآن (الدفع الآمن عبر Stripe)")
    service_price = 100.00
    
    if st.button("ادفع الآن بقيمة 100 USD"):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'خدمة استشارية / برمجية',
                        },
                        'unit_amount': int(service_price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://streamlit.io?success=true',
                cancel_url='https://streamlit.io?canceled=true',
            )
            st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_session.url}">', unsafe_allow_html=True)
            st.success("جاري تحويلك إلى صفحة الدفع الآمنة...")
        except Exception as e:
            st.error(f"حدث خطأ أثناء إنشاء رابط الدفع: {e}")

with tab2:
    st.subheader("👥 إدارة العملاء")
    st.write("قائمة العملاء المسجلين ستظهر هنا.")

with tab3:
    st.subheader("💳 لوحة المالية الحقيقية")
    sales_data = []
    try:
        res = supabase.table("sales").select("*").execute()
        sales_data = res.data if res else []
        st.success("تم الاتصال وجلب البيانات بنجاح!")
    except Exception as e:
        st.error(f"خطأ قاعدة البيانات التفصيلي: {e}")
        sales_data = []
    
    total_sales = sum(float(item.get('amount', 0)) for item in sales_data) if sales_data else 0
    total_deals = len(sales_data) if sales_data else 0
    
    col1, col2 = st.columns(2)
    col1.metric("إجمالي الصفقات المغلقة", f"{total_deals} صفقة")
    col2.metric("إجمالي الأرباح المحصلة", f"${total_sales:,.2f} USD")
    
    st.write("---")
    st.write("البيانات يتم تحديثها مباشرة من قاعدة البيانات.")
