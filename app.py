import streamlit as st
from engine import AutonomousEngine
from wallet_manager import WalletManager

engine = AutonomousEngine()
wallet = WalletManager()

st.set_page_config(page_title="GrowthEngine | Autonomous B2B System", layout="wide")

st.title("🎯 GrowthEngine: نظام الاستحواذ التلقائي على العملاء")
st.write("أدخل بيانات شركتك أو مجالك لكي يقوم النظام بتشخيص الفجوات الرقمية وإظهار حجم الأرباح الضائعة.")

# مدخلات العميل الذكية
col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("مجال الشركة أو نشاطك (مثال: Real Estate, Software Agency):")
with col2:
    company_size = st.selectbox("حجم الشركة:", ["ناشئة", "متوسطة", "كبيرة"])

if st.button("🚀 تشخيص الفجوات وعرض التقرير الشامل"):
    if niche:
        report = engine.generate_growth_report(niche, company_size)
        
        st.divider()
        st.subheader("📊 تقرير التشخيص الاستراتيجي")
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="العملاء المحتملين الضائعين شهرياً", value=report['lost_leads'])
        with m2:
            st.metric(label="حجم الخسارة المالية الشهرية", value=report['estimated_loss'])
            
        st.warning(f"⚠️ **نتيجة الفحص:** {report['diagnostic']}")
        st.info(f"💡 **الحل المقترح:** {report['recommended_action']}")
        
        st.divider()
        st.subheader("🔒 تفعيل النظام الآلي الكامل (الاستحواذ التلقائي)")
        st.write("لإطلاق النظام ليعمل بشكل ذاتي تماماً ويجلب هؤلاء العملاء إلى محفظتك، يتم تفعيل العقد الذكي للخدمة الشاملة بقيمة **$5,000**.")
        
        # عرض محفظتك لإتمام التحويل الفوري
        st.code("Trust Wallet Address (USDT / Crypto): 0xYourTrustWalletAddressHere")
        st.success("بمجرد إتمام التحويل، سيقوم النظام بربط عقدتك الذكية وبدء مهام الاستحواذ تلقائياً في الخلفية.")
    else:
        st.error("يرجى إدخال مجال العمل للبدء بعملية التشخيص.")
