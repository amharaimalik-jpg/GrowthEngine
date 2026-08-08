import streamlit as st
from engine import AutonomousEngine
from wallet_manager import WalletManager

engine = AutonomousEngine()
wallet = WalletManager()

st.set_page_config(page_title="GrowthEngine | B2B Acquisition", layout="wide")

st.title("🎯 GrowthEngine: نظام الاستحواذ التلقائي على العملاء")
st.write("أدخل مجال عملك (Niche) وسيقوم النظام فوراً بتحليل فرص النمو المفقودة.")

niche = st.text_input("مجال العمل (مثال: Real Estate, SaaS, Digital Agency):")

if st.button("تحليل الفجوة والفرص"):
    if niche:
        analysis = engine.analyze_market_gap(niche)
        st.success(f"تم العثور على {analysis['leads_identified']} فرصة نمو في مجال {analysis['niche']}!")
        st.metric("الأرباح المتوقعة من الفرص:", analysis['projected_revenue'])
        st.info("لإطلاق النظام للعمل تلقائياً وجلب هذه الفرص إلى محفظتك، يرجى إتمام تفعيل العقد الذكي.")
        
        # هنا مكان الدفع
        st.subheader("تفعيل خدمة الإدارة الكاملة ($5,000)")
        st.code("Wallet Address: 0xYourTrustWalletAddressHere")
        st.warning("بعد التحويل، سيقوم النظام تلقائياً ببدء حملة الاستحواذ على العملاء.")
    else:
        st.error("يرجى إدخال المجال للبدء.")
