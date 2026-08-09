import streamlit as st
from engine import AutonomousEngine, generate_growth_report

st.set_page_config(page_title="GrowthEngine", layout="wide")

st.title("🎯 نظام الاستحواذ والتوسع الذاتي (حقيقي)")
st.markdown("محرك رقمي متكامل لتشخيص فجوات الشركات، توليد حملات الانتشار، وإدارة التحويلات المالية الحقيقية.")

# المدخلات
col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("مجال الشركة المستهدفة (مثال: Real Estate, SaaS):")
with col2:
    company_size = st.selectbox("حجم النشاط:", ["ناشئة", "متوسطة", "منشأة كبرى"])

if st.button("🚀 تشغيل محرك التشخيص والانتشار التلقائي"):
    if niche:
        with st.spinner("جاري فحص السوق وتوليد التقرير الذكي..."):
            report = generate_growth_report(niche, company_size)
            st.markdown(report)
            
            # تفعيل المحرك المالي
            engine = AutonomousEngine()
            status, msg = engine.check_payment_status()
            st.info(f"حالة النظام المالي: {msg}")
    else:
        st.warning("يرجى إدخال مجال الشركة المستهدفة أولاً.")
