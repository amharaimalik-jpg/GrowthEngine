import streamlit as st
from engine import AutonomousEngine

engine = AutonomousEngine()

st.set_page_config(page_title="GrowthEngine | Live B2B System", layout="wide")

st.title("🎯 GrowthEngine: نظام الاستحواذ والتوسع الذاتي (حقيقي)")
st.write("محرك رقمي متكامل لتشخيص فجوات الشركات، توليد حملات الانتشار، وإدارة التحويلات المالية الحقيقية.")

# مدخلات العميل الذكية
col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("مجال الشركة المستهدفة (مثال: Real Estate, SaaS):")
with col2:
    company_size = st.selectbox("حجم النشاط:", ["ناشئة", "متوسطة", "كبيرة"])

if st.button("🚀 تشغيل محرك التشخيص والانتشار التلقائي"):
    if niche:
        report = engine.generate_growth_report(niche, company_size)
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
        st.subheader("🧬 أصول الانتشار والاستهداف المولدّة ذاتياً")
        st.text_area("نص النشر المجتمعي (Viral Post):", assets['viral_post'])
        st.text_area("نص الاستهداف المباشر (Cold Outreach):", assets['cold_email'])
        
        st.divider()
        st.subheader("🔒 تفعيل النظام الآلي الكامل (العقد الحقيقي بقيمة $5,000)")
        st.write("لإطلاق النظام وبدء الاستحواذ الفعلي لصالح العميل، يرجى إتمام تحويل قيمة الخدمة (5,000 USDT) حصراً عبر شبكة **BEP20** إلى عنوان محفظتك الرسمي أدناه:")
        
        # عرض عنوان محفظتك الحقيقي الذي أرسلته
        st.code("0xD7709Dc72614240B065416D17c662Ee124654c78")
        st.success("بمجرد إرسال المبلغ من قبل العميل وتأكيده على شبكة البلوكشين، ستصل الأموال فوراً إلى تطبيق Trust Wallet الخاص بك.")
    else:
        st.error("يرجى إدخال مجال العمل للبدء.")
