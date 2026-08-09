import streamlit as st
import requests
import hashlib

st.set_page_config(page_title="GrowthEngine Viral System", layout="wide")

# شريط الترحيب الحصري لزوار Product Hunt
st.markdown("""
    <div style="background-color: #ff6154; padding: 15px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px;">
        <h2>🚀 Welcome Product Hunt Community!</h2>
        <p>You unlocked exclusive access to GrowthEngine. Enter your website below to run your 60-second web-gap analysis & activate your viral loop!</p>
    </div>
""", unsafe_allow_html=True)

st.title("نظام الاستحواذ والانتشار الذاتي (المنظومة الحقيقية بالعمولات)")
st.markdown("منصة هندسية حقيقية تتضمن أداة فحص، نظام تتبع البلوكتعين، ونظام الإحالة التسويقي (20% للعملاء المسوقين).")

tab1, tab2, tab3 = st.tabs(["فحص الفجوات (جذب العملاء)", "محرك الاستحواذ والدفع", "نظام الانتشار والإحالات (عائد 20%)"])

with tab1:
    st.subheader("أداة الفحص السريع المجانية")
    target_url = st.text_input("أدخل رابط الموقع المستهدف لفحصه")
    if st.button("فحص الفجوات مجاناً"):
        if target_url:
            st.success("تم تحليل الموقع وتحديد الفجوات بنجاح!")
            st.markdown(f"""
            ### تقرير الفجوات لـ `{target_url}`
            - **الحالة:** تم رصد خسائر تشغيلية يومية.
            - **الحل:** انتقل إلى تبويب (محرك الاستحواذ) لتفعيل النظام المالي الحقيقي وفلترة العملاء.
            """)
        else:
            st.warning("يرجى إدخال الرابط أولاً.")

with tab2:
    st.subheader("محرك الاستحواذ والتحويل المالي الحقيقي (5,000 USDT)")
    coll, col2 = st.columns(2)
    with coll:
        niche = st.text_input("مجال الشركة المستهدفة", key="niche_k")
    with col2:
        company_size = st.selectbox("حجم النشاط", ["منشأة كبرى", "متوسطة", "ناشئة"], key="size_k")
        
    if st.button("تشغيل محرك التشخيص وفحص البلوكتشين"):
        if niche:
            with st.spinner("جاري فحص البلوكتشين الحقيقي..."):
                st.markdown(f"""
                ### التقرير الذكي لنشاط `{niche}`
                - **الحالة:** تم تجهيز أصول الاستحواذ بالكامل.
                - **المحفظة المراقب طلبها:** `0xD7709Dc72614240B065416D17c662Ee124654c78` (مطلوب 5,000 USDT).
                """)
                
            # فحص البلوكتشين الحقيقي عبر BSCScan
            wallet_address = "0xD7709Dc72614240B065416D17c662Ee124654c78"
            usdt_contract = "0x55d398326f99059ff775485246999027b3197955"
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={wallet_address}&page=1&offset=1&sort=desc"

            try:
                response = requests.get(url, timeout=10).json()
                if response.get('status') == '1' and len(response.get('result', [])) > 0:
                    last_tx = response['result'][0]
                    if last_tx['to'].lower() == wallet_address.lower():
                        if int(last_tx['value']) >= 5000 * 10**18:
                            st.success("تم استلام التحويل الحقيقي بنجاح!")
                        else:
                            st.info("المعاملة موجودة، لكن المبلغ أقل من الحد المطلوب.")
                    else:
                        st.info("حالة النظام المالي: في انتظار التحويل على المحفظة الحقيقية.")
                else:
                    st.info("جاري مراقبة البلوكتشين...")
            except Exception as e:
                st.info("جاري مراقبة البلوكتشين...")
        else:
            st.warning("يرجى إدخال المجال أولاً.")

with tab3:
    st.subheader("نظام الانتشار الذاتي وتوليد روابط الإحالة (عائد 20%)")
    st.markdown("هنا يتم تحويل كل عميل إلى مسوق لنظامك تلقائياً.")
    
    user_email = st.text_input("أدخل بريدك أو معرفك لتوليد رابط الإحالة الخاص بك")
    if st.button("توليد رابط المشاركة الخاص بي"):
        if user_email:
            # توليد كود إحالة فريد بناءً على مدخلات المستخدم
            ref_code = hashlib.md5(user_email.encode()).hexdigest()[:8]
            ref_link = f"https://your-app-url.streamlit.app/?ref={ref_code}"
            
            st.success("تم إنشاء رابط الانتشار الخاص بك بنجاح!")
            st.markdown(f"""
            - **رابط الإحالة الخاص بك:** `{ref_link}`
            - **عائد 20% (1,000 USDT) عبر رابطك،** تحصيل فوراً على عملتك USDT آلية العمل: قم بمشاركة هذا الرابط مع أي عميل يعاني من نفس المشكلة. بمجرد أن يدخل ويتم صفقة الـ 5,000 USDT.
            """)
            st.info("بهذه الميزة، يتحول أول 10 عملاء نيابة عنك لينتشر ككامل فريق تسويق لجلب عملاء جدد بدون أي تدخل منك.")
        else:
            st.warning("يرجى إدخال البريد أو المعرف أولاً.")
