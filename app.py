import streamlit as st
import pandas as pd
import time
from engine import AutonomousEngine
from wallet_manager import WalletManager

# تهيئة الأنظمة الفرعية
engine = AutonomousEngine()
wallet = WalletManager()
health = engine.get_system_health()
node_info = wallet.get_node_info()

# إعدادات الصفحة الأساسية للنظام الذكي
st.set_page_config(
    page_title="Malik Autonomous Engine - النظام الذكي المتكامل",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 محطة التشغيل الذكي والأتمتة المتكاملة")
st.success(f"النظام يعمل بكفاءة تامة | العقدة النشطة: {node_info['node']} | الأمان: {health['encryption']}")

# لوحة التحكم الجانبية
st.sidebar.header("⚙️ مركز التحكم بالعمليات")
mode = st.sidebar.selectbox("اختر وضع التشغيل:", ["الوضع التلقائي بالكامل", "وضع المراقبة الحية"])
auto_refresh = st.sidebar.checkbox("تفعيل التشغيل المستمر (Auto-Pilot)", value=True)

# واجهة معالجة الأصول السريعة في الشريط الجانبي
st.sidebar.divider()
st.sidebar.subheader("🔀 وحدة توجيه الأصول")
input_amount = st.sidebar.number_input("أدخل القيمة للمعالجة الذاتية:", min_value=100, max_value=100000, value=5000)

if st.sidebar.button("تنفيذ التوجيه والتحويل الرقمي"):
    result = wallet.process_asset_routing(input_amount)
    st.sidebar.success(f"تم بنجاح! المبلغ المعالج: {result['routed_amount']} (معرف: {result['routing_id']})")

# الواجهة الرئيسية للمراقبة
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="حالة النظام ومعدل التشغيل", value=health["uptime"], delta="مستقر وآمن")

with col2:
    st.metric(label="حالة الأصول والعقدة", value=node_info["state"], delta="بدون تدخل بشري")

with col3:
    st.metric(label="مستوى التشفير والأمان", value=health["encryption"], delta="حماية تامة")

st.divider()

st.subheader("📊 لوحة رصد الأداء والتدفقات اللحظية")

# محاكاة تدفق العمليات والأرباح الذاتية
chart_data = pd.DataFrame({
    'الوقت': ['01:00', '01:05', '01:10', '01:15', '01:20'],
    'كفاءة التنفيذ الذاتي (%)': [98.5, 99.1, 99.7, 100.0, 100.0],
    'التدفق النقدي المؤتمت': [1200, 2400, 3900, 5200, 7500]
})

st.line_chart(chart_data.set_index('الوقت'))

# زر تنفيذ بروتوكول الالتفاف والتحسين الفوري
if st.button("⚡ تنفيذ بروتوكول الالتفاف والتحسين الذكي الآن"):
    action_result = engine.execute_logic_bypass()
    st.toast(f"تم بنجاح: {action_result}")
    st.info("النظام يقوم بالمعالجة والتحويل في الخلفية تلقائياً وبشكل كامل.")
