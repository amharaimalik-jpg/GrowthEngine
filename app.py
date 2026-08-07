import streamlit as st
from supabase import create_client
import stripe
import re

# إعداد الصفحة
st.set_page_config(page_title="Growth Engine - النظام الشامل", page_icon="🚀", layout="wide")

# تنظيف والاتصال بقاعدة البيانات والـ Stripe
raw_url = str(st.secrets.get("SUPABASE_URL", ""))
raw_key = str(st.secrets.get("SUPABASE_KEY", ""))
url = re.sub(r'[\s"\'`]', '', raw_url)
key = re.sub(r'[\s"\'`]', '', raw_key)

supabase = create_client(url, key)
stripe.api_key = st.secrets.get("STRIPE_API_KEY", "")

# جلب بيانات العملاء والصفقات من جدول sales
@st.cache_data(ttl=2)
def fetch_sales_data():
    try:
        res = supabase.table("sales").select("*").execute()
        return res.data if res else []
    except:
        return []

sales_data = fetch_sales_data()

# تصميم التبويبات الرئيسية للتطبيق
tab1, tab2, tab3 = st.tabs([
    "🚀 الرئيسية وخدمة الرد الآلي", 
    "👥 العملاء والتفاوض والصفقات", 
    "💳 اللوحة المالية والأرباح"
])

with tab1:
    st.subheader("🚀 لوحة التحكم والخدمات الأساسية")
    st.write("مرحباً بك في نظامك المتكامل لإدارة الأعمال، تحصيل المدفوعات، والرد الآلي على العملاء.")
    
    col_pay, col_chat = st.columns(2)
    
    with col_pay:
        st.markdown("### 💳 اطلب الخدمة الآن ($2,000 USD)")
        service_price = 2000.00  # سعر الخدمة المطلوب
        
        st.info("💡 الخدمة الاحترافية متكاملة وتشمل الأتمتة، الربط البرمجي، والدعم الكامل بقيمة 2,000 دولار.")
        
        if st.button("ادفع الآن بقيمة 2,000 USD عبر Stripe"):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'النظام البرمجي والاستشاري المتكامل',
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

    with col_chat:
        st.markdown("### 🤖 مساعد الذكاء الاصطناعي للإجابة على استفسارات العملاء")
        st.write("جرب الرد الفوري والدقيق على استفسارات العملاء المحتملين:")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "مرحباً! أنا مساعدك الذكي. كيف يمكنني مساعدتك في تفاصيل خدمتنا البرمجية؟"}
            ]
            
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
        if prompt := st.chat_input("اكتب استفسار العميل هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
                
            # إجابات ذكية متكاملة ودقيقة
            answer = "نحن نقدم نظاماً متكاملاً لإدارة الأعمال والمدفوعات بقيمة 2,000 دولار، يشمل الإعداد الكامل، لوحة مالية، ونظام متابعة العملاء بدقة."
            if "سعر" in prompt or "تكلفة" in prompt or "كم" in prompt:
                answer = "تكلفة الخدمة الشاملة هي 2,000 دولار أمريكي، وتتضمن الإعداد والتشغيل والربط الكامل مع بوابات الدفع."
            elif "ميزات" in prompt or "يشمل" in prompt:
                answer = "تشمل الخدمة: لوحة مالية حقيقية، نظام تتبع العملاء، معالجة مدفوعات آمنة عبر Stripe، ومساعد ذكي للرد على الاستفسارات."
                
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)

with tab2:
    st.subheader("👥 إدارة العملاء ومتابعة حالات الصفقات")
    st.write("رؤية تفصيلية للعملاء وتصنيفهم بين قيد التفاوض والصفقات الناجحة:")
    
    col_negotiate, col_closed = st.columns(2)
    
    with col_negotiate:
        st.markdown("### 🔄 العملاء قيد التفاوض (Pending / Leads)")
        # فحص العملاء الذين حالتهم غير مدفوعة أو قيد المعالجة
        negotiating_list = [item for item in sales_data if str(item.get('status', '')).lower() != 'paid']
        if negotiating_list:
            for client in negotiating_list:
                c_name = client.get('client_name', 'عميل محتمل')
                c_amt = client.get('amount', 2000)
                st.warning(f"👤 **{c_name}** | القيمة المتوقعة: ${c_amt:,.2f} USD")
        else:
            st.write("لا توجد صفقات معلقة أو قيد التفاوض حالياً في القاعدة.")
            
    with col_closed:
        st.markdown("### ✅ العملاء الذين تمت الصفقة معهم (Closed / Paid)")
        # العملاء الذين تمت صفقتهم بنجاح
        closed_list = [item for item in sales_data if item.get('amount') is not None]
        if closed_list:
            for client in closed_list:
                c_name = client.get('client_name', f"عميل رقم {client.get('id')}")
                c_amt = client.get('amount', 2000)
                st.success(f"🎉 **{c_name}** | تم إتمام الصفقة بمبلغ: ${c_amt:,.2f} USD")
        else:
            st.write("لا توجد صفقات مكتملة حالياً.")

with tab3:
    st.subheader("💳 اللوحة المالية والأرباح المحصلة الحقيقية")
    
    total_sales = 0
    for item in sales_data:
        val = item.get('amount')
        if val is not None:
            try:
                total_sales += float(val)
            except:
                pass
                
    total_deals = len(sales_data)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("إجمالي الصفقات الناجحة", f"{total_deals} صفقة")
    m2.metric("إجمالي الأرباح المحصلة", f"${total_sales:,.2f} USD")
    m3.metric("سعر الخدمة القياسي", "$2,000.00 USD")
    
    st.write("---")
    st.markdown("### 📊 جدول البيانات الحي من قاعدة البيانات (Supabase)")
    if sales_data:
        st.dataframe(sales_data, use_container_width=True)
    else:
        st.warning("قاعدة البيانات فارغة حالياً. أضف بيانات في جدول sales لتراها هنا فوراً.")
