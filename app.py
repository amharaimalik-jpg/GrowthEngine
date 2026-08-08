import streamlit as st
from engine import AutonomousEngine
from wallet_manager import WalletManager

engine = AutonomousEngine()
wallet = WalletManager()

st.set_page_config(page_title="GrowthEngine | Autonomous B2B System", layout="wide")

st.title("🎯 GrowthEngine: نظام الاستحواذ والتوسع الذاتي")
st.write("محرك رقمي متكامل لتشخيص فجوات الشركات، توليد حملات الانتشار، وإدارة التحويلات المالية ذاتياً.")

# مدخلات العميل الذكية
col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("مجال الشركة المستهدفة (مثال: Real Estate, SaaS):")
with col2:
    company_size = st.selectbox("حجم النشاط:", ["ناشئة", "متوسطة", "كبيرة"])

if st.button("🚀 تشغيل محرك التشخيص والانتشار التلقائي"):
    if niche:
        # توليد التقرير
        report = engine.generate_growth_report(niche, company_size)
        # توليد محتوى الانتشار والاستهداف (المساران مزعوران في الكود)
        assets = engine.generate_outreach_assets(niche)
        
        st.divider()
        st.subheader("📊 تقرير التشخيص الاستراتيجي للعميل")
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="العملاء المحتملين الضائعين شهرياً", value=report['lost_leads'])
        with m2:
            st.metric(label="حجم الخسارة المالية الشهرية", value=report['estimated_loss'])
            
        st.warning(f"⚠️ **نتيجة الفحص:** {report['diagnostic']}")
        
        st.divider()
        st.subheader("🧬 أصول الانتشار والاستهداف المولدّة ذاتياً بواسطة النظام")
        st.write("هذه النصوص يتم إنشاؤها تلقائياً بواسطة المحرك لضمان الانتشار بدون تدخل بشري:")
        st.text_area("نص النشر المجتمعي (Viral Post):", assets['viral_post'])
        st.text_area("نص الاستهداف المباشر (Cold Outreach):", assets['cold_email'])
        
        st.divider()
        st.subheader("🔒 تفعيل النظام الآلي الكامل (الاستحواذ التلقائي)")
        st.write("لإطلاق النظام ليعمل بشكل ذاتي تماماً ويجلب هؤلاء العملاء إلى محفظتك، يتم تفعيل العقد الذكي للخدمة الشاملة بقيمة **$5,000**.")
        
        # عرض محفظتك لإتمام التحويل الفوري
        st.code("Trust Wallet Address (USDT / Crypto): 0xYourTrustWalletAddressHere")
        st.success("بمجرد إتمام التحويل، سيقوم النظام بربط عقدتك الذكية وبدء مهام الاستحواذ تلقائياً في الخلفية.")
    else:
        st.error("يرجى إدخال مجال العمل للبدء.")
