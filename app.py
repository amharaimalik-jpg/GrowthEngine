import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Growth Engine - My Real Wallet",
    page_icon="💎",
    layout="wide",
)

DB_NAME = "real_wallet_engine.db"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_email TEXT,
            amount REAL,
            status TEXT,
            outreach_status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

MY_EXACT_WALLET = "TQWzQdUhanott9zGsnjU2KFYscxWYgLL"

with st.sidebar:
    st.header("⚙️ إعدادات الوكيل الآلي")
    gemini_key = st.text_input("مفتاح Gemini API:", type="password")
    my_email = st.text_input("بريدك الإلكتروني:", value="amharaimalik@gmail.com")
    my_pass = st.text_input("كلمة مرور التطبيق (App Password):", type="password")
    
    st.markdown("---")
    st.subheader("💎 محفظة Trust Wallet (TRC20)")
    wallet_address = st.text_input("العنوان المعتمد:", value=MY_EXACT_WALLET)
    st.success("🟢 تم تثبيت عنوان محفظتك الحقيقي بنجاح.")

def send_email(target_email, subject, message, sender_email, sender_pass, wallet):
    full_msg = f"{message}\n\n-----------------------------------\nلتأكيد التعاقد وبدء العمل، يرجى تحويل مبلغ $2000 USDT (شبكة TRC20) إلى محفظتي الرسمية التالية:\n{wallet}\n-----------------------------------"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(full_msg, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_pass)
        server.send_message(msg)
        server.quit()
        return True, "تم الإرسال"
    except Exception as e:
        return False, str(e)

st.title("💎 Growth Engine - الإدخال المباشر للشركات الحقيقية")
st.success("🟢 النظام جاهز تماماً. أضف الشركات المستهدفة وسيتكفل النظام بإرسال العروض وعنوان محفظتك وقيمة 2000$.")

def get_data():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT client_name, client_email, amount, status, outreach_status FROM sales")
    rows = cursor.fetchall()
    conn.close()
    return [{"client_name": r[0], "client_email": r[1], "amount": r[2], "status": r[3], "outreach_status": r[4]} for r in rows]

data = get_data()
closed = [i for i in data if i["status"] == "paid"]
total = sum(float(i["amount"]) for i in closed)

c1, c2, c3, c4 = st.columns(4)
c1.metric("الشركات المرصودة", f"{len(data)} شركة")
c2.metric("حالة الوكيل", "جاهز للتنفيذ 🤖")
c3.metric("العقود المدفوعة", f"{len(closed)} عقد")
c4.metric("الأرباح المحصلة", f"${total:,.2f} USD")

st.markdown("---")

st.subheader("➕ إضافة شركة حقيقية للجدول فورا")
with st.form("add_client"):
    c_name_input = st.text_input("اسم الشركة الحقيقية (مثال: Vortex Tech):")
    c_email_input = st.text_input("البريد الإلكتروني للشركة:")
    submitted = st.form_submit_button("إضافة الشركة وتثبيت عقد 2000$ 🟢")
    if submitted and c_name_input and c_email_input:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales (client_name, client_email, amount, status, outreach_status) VALUES (?, ?, ?, ?, ?)",
                       (c_name_input, c_email_input, 2000.0, "lead", "جاهز للإرسال 🟢"))
        conn.commit()
        conn.close()
        st.success("✅ تمت إضافة الشركة بنجاح وظهرت في الجدول بالأسفل!")
        st.rerun()

st.markdown("---")
st.subheader("🌐 جدول العمليات والشركات المستهدفة")
if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True)
    
    if st.button("🚀 إرسال العروض وعنوان محفظتك لكل الشركات المضافة", type="primary"):
        if not my_email or not my_pass:
            st.error("⚠️ يرجى إدخال بيانات الـ Gmail في الشريط الجانبي.")
        else:
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT client_name, client_email FROM sales WHERE status != 'paid'")
            targets = cursor.fetchall()
            
            sent_count = 0
            for name, email in targets:
                default_msg = f"عزيزي فريق شركة {name},\n\nنود عرض شراكة استراتيجية لتطوير وتنفيذ أنظمة هندسة البرمجيات المتقدمة لشركتكم بكفاءة عالية."
                success, _ = send_email(
                    target_email=email,
                    subject=f"شراكة استراتيجية تقنية لشركة {name}",
                    message=default_msg,
                    sender_email=my_email,
                    sender_pass=my_pass,
                    wallet=wallet_address
                )
                if success:
                    cursor.execute("UPDATE sales SET outreach_status = ? WHERE client_email = ?", ("تم إرسال العرض وعنوان المحفظة 🟢", email))
                    sent_count += 1
                    
            conn.commit()
            conn.close()
            st.success(f"🚀 تم إرسال العروض لـ {sent_count} شركة بنجاح!")
            st.rerun()
else:
    st.info("لا توجد شركات مسجلة حالياً. استخدم نموذج الإضافة بالأعلى لإضافة شركة وابدأ العمل فوراً.")

st.markdown("---")
st.subheader("💳 تأكيد تحصيل الأموال في محفظتك")
if data:
    unpaid = [d["client_name"] for d in data if d["status"] != "paid"]
    if unpaid:
        chosen = st.selectbox("اختر الشركة التي حولت الـ 2000$ إلى محفظتك:", unpaid)
        if st.button("💰 تأكيد استلام الـ 2000$ في محفظتي"):
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("UPDATE sales SET status = ?, outreach_status = ? WHERE client_name = ?", 
                           ("paid", "تم التحويل لمحظتك بنجاح 🟢", chosen))
            conn.commit()
            conn.close()
            st.success("🎉 تم تحديث رصيد أرباحك الفعلية بنجاح!")
            st.rerun()
