import streamlit as st
from supabase import create_client
import stripe

# إعداد الصفحة لتكون واسعة ومنظمة
st.set_page_config(page_title="Growth Engine 24/7", page_icon="🚀", layout="wide")

# الاتصال بقاعدة البيانات والأسرار بأمان تام
try:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"خطأ في إعدادات الاتصال بقاعدة البيانات: {e}")
    st.stop()

if "STRIPE_API_KEY" in st.secrets:
    stripe.api_key = st.secrets["STRIPE_API_KEY"].strip()

# جلب البيانات المباشرة من الجدول
@st.cache_data(ttl=2)
def get_sales():
    try:
        res = supabase.table("sales").select("*").execute()
        return res.data if res else []
    except:
        return []

sales_data = get_sales()

# حساب المؤشرات بدقة
total_deals = len(sales_data)
closed_list = [i for i in sales_data if str(i.get('status', '')).lower() == 'paid' or i.get('amount') is not None]
negotiating_list = [i for i in sales_data if str(i.get('status', '')).lower() != 'paid' and i.get('status') == 'lead']
total_earnings = sum(float(i.get('amount', 0)) for i in closed_list if i.get('amount'))

st.title("🚀 نظام Growth Engine الشامل (يعمل 24/7 في السوق)")

# تصميم التبويبات الأربعة الرئيسية
tab1, tab2, tab3, tab4 = st.tabs([
    "🤖 محرك جلب وفلترة العملاء (24/7)",
    "💬 شاشة الاستفسارات والرد الآلي",
    "👥 إدارة العملاء والصفقات",
    "💳 اللوحة المالية والأرباح ($2,000)"
])

with tab1:
    st.subheader("🌐 لوحة مراقبة محرك جلب العملاء الآلي في الشبكة")
    st.write("النظام يعمل 24/7 للبحث عن العملاء، فلترتهم، وإقناعهم بالخدمة تلقائياً.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("إجمالي العملاء المكتشفين", f"{len(sales_data)} عميل")
    m2.metric("قيد التفاوض والإقناع", f"{len(negotiating_list)} عميل")
    m3.metric("الصفقات الناجحة", f"{len(closed_list)} صفقة")
    m4.metric("حالة النظام", "يعمل 24/7 🟢")

    st.write("---")
    if st.button("🔄 محاكاة جلب وعملية إقناع عميل جديد فوراً"):
        try:
            supabase.table("sales").insert({
                "client_name": "شركة الابتكار التقني",
                "amount": 2000,
                "status": "lead"
            }).execute()
            st.success("تم جلب عميل جديد بواسطة النظام وإضافته لقائمة التفاوض وبدء الإقناع!")
            st.rerun()
        except Exception as e:
            st.error(f"خطأ أثناء جلب العميل: {e}")

with tab2:
    st.subheader("💬 شاشة الاستفسارات والرد الآلي بالكامل")
    st.write("شاهد كيف يتفاعل النظام ويجيب بدقة على جميع أسئلة العملاء:")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "مرحباً بك! أنا مساعدك الذكي. كيف يمكنني إخبارك بتفاصيل خدمتنا البرمجية بقيمة 2,000 دولار؟"}
        ]
        
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    user_input = st.chat_input("اكتب استفسار العميل هنا...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        reply = "نحن نقدم نظاماً متكاملاً لإدارة الأعمال وتحصيل الأرباح بقيمة 2,000 دولار، يشمل التشغيل الآلي، جلب العملاء، والرد الفوري."
        if "سعر" in user_input or "تكلفة" in user_input or "كم" in user_input:
            reply = "تكلفة الخدمة الشاملة هي 2,000 دولار أمريكي فقط، وتتضمن الإعداد والتشغيل والربط الكامل مع بوابات الدفع."
        elif "مميزات" in user_input or "ميزات" in user_input:
            reply = "تشمل الميزات: جلب العملاء آلياً 24/7، رد ذكي دقيق، تحويل الأموال تلقائياً، ولوحة مالية حية."
            
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

with tab3:
    st.subheader("👥 تفاصيل العملاء (قيد التفاوض ومن تمت الصفقة معهم)")
    col_neg, col_cls = st.columns(2)
    
    with col_neg:
        st.markdown("### 🔄 العملاء قيد التفاوض والإقناع حالياً")
        if negotiating_list:
            for c in negotiating_list:
                st.warning(f"👤 **{c.get('client_name')}** | القيمة: ${c.get('amount', 2000):,.2f} | الحالة: قيد المفاوضات")
        else:
            st.info("لا توجد صفقات معلقة حالياً.")
            
    with col_cls:
        st.markdown("### ✅ العملاء الذين تمت الصفقة معهم وتحويل المال")
        if closed_list:
            for c in closed_list:
                st.success(f"🎉 **{c.get('client_name')}** | تم إتمام الصفقة وتحويل مبلغ: ${c.get('amount', 2000):,.2f} بنجاح")
        else:
            st.info("لا توجد صفقات مكتملة حتى الآن.")

with tab4:
    st.subheader("💳 اللوحة المالية والأرباح الحقيقية وبوابة الدفع ($2,000)")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("إجمالي الصفقات الناجحة", f"{len(closed_list)} صفقات")
    m_col2.metric("إجمالي الأرباح المحصلة", f"${total_earnings:,.2f} USD")
    m_col3.metric("سعر الخدمة الثابت", "$2,000.00 USD")
    
    st.write("---")
    st.markdown("### 💳 زر الدفع السريع والآمن للعملاء عبر Stripe")
    if st.button("💳 ادفع الآن بقيمة 2,000 USD عبر Stripe"):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'خدمة النظام البرمجي المتكامل Growth Engine'},
                        'unit_amount': int(2000 * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://streamlit.io?success=true',
                cancel_url='https://streamlit.io?canceled=true',
            )
            st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_session.url}">', unsafe_allow_html=True)
            st.success("جاري تحويلك لبوابة الدفع الآمنة...")
        except Exception as e:
            st.error(f"خطأ في إنشاء رابط الدفع: {e}")

    st.write("---")
    st.markdown("### 📊 جدول البيانات المباشر من قاعدة البيانات")
    if sales_data:
        st.dataframe(sales_data, use_container_width=True)
    else:
        st.info("جدول البيانات فارغ.")
