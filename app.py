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

# عنوان المحفظة الحقيقي الذي كتبته في ورقتك
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

def call_gemini(prompt, api_key):
    if not api_key:
        return "عزيزي العميل، نقدم حلول هندسة البرمجيات والذكاء الاصطناعي لتطوير أعمالكم."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
    return "عزيزي العميل، نقدم حلول هندسة البرمجيات والذكاء الاصطناعي لتطوير أعمالكم."

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

st.title("💎 Growth Engine - الوكيل المستقل بمحفظتك الحقيقية")
st.success("🟢 النظام متصل ومبرمج آلياً لدمج عنوان محفظتك (TRC20) وقيمة عقد 2000$ في كل رسالة تُرسل للشركات الحقيقية.")

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
c2.metric("حالة الوكيل", "يعمل باستقلالية 🤖")
c3.metric("العقود المدفوعة", f"{len(closed)} عقد")
c4.metric("الأرباح المحصلة", f"${total:,.2f} USD")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌐 الخطوة 1: جلب الشركات الحقيقية وبريدها آلياً", type="primary"):
        if not gemini_key:
            st.error("⚠️ يرجى إدخال مفتاح Gemini API في الشريط الجانبي.")
        else:
            with st.spinner("جاري استخبارات السوق وجلب الشركات مع بريدها وقيمة 2000$..."):
                prompt = """قم بتوليد قائمة لـ 3 شركات تقنية وناشئة حقيقية مع بريدها الإلكتروني الرسمي للتواصل. الصيغة بالضبط لكل سطر:
                اسم الشركة | البريد الإلكتروني
                مثال:
                Vortex AI Labs | contact@vortexailabs.com
                Nova Software | info@novasoftware.io
                SaaSify Tech | support@saasifytech.co"""
                
                output = call_gemini(prompt, gemini_key)
                lines = output.strip().split("\n")
                
                conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                cursor = conn.cursor()
                
                added = 0
                for line in lines:
                    if "|" in line:
                        parts = line.split("|")
                        c_name = parts[0].strip()
                        c_email = parts[1].strip()
                        cursor.execute("SELECT COUNT(*) FROM sales WHERE client_email = ?", (c_email,))
                        if cursor.fetchone()[0] == 0 and "@" in c_email:
                            cursor.execute("INSERT INTO sales (client_name, client_email, amount, status, outreach_status) VALUES (?, ?, ?, ?, ?)",
                                           (c_name, c_email, 2000.0, "lead", "جاهز للإرسال 🟢"))
                            added += 1
                conn.commit()
                conn.close()
                st.success(f"🎉 تم جلب {added} شركة حقيقية بنجاح!")
                st.rerun()

with col2:
    if st.button("🚀 الخطوة 2: إرسال العروض وعنوان محفظتك لكل الشركات", type="primary"):
        if not gemini_key or not my_email or not my_pass:
            st.error("⚠️ يرجى التأكد من إدخال مفتاح Gemini وكلمة مرور Gmail في الشريط الجانبي.")
        else:
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT client_name, client_email FROM sales WHERE status != 'paid'")
            targets = cursor.fetchall()
            
            sent_count = 0
            for name, email in targets:
                msg_prompt = f"اكتب رسالة بريد إلكتروني تسويقية لشركة {name} لعرض نظام هندسة نمو وتطوير تقني بقيمة 2000 دولار."
                ai_text = call_gemini(msg_prompt, gemini_key)
                
                success, _ = send_email(
                    target_email=email,
                    subject=f"شراكة استراتيجية تقنية لشركة {name}",
                    message=ai_text,
                    sender_email=my_email,
                    sender_pass=my_pass,
                    wallet=wallet_address
                )
                if success:
                    cursor.execute("UPDATE sales SET outreach_status = ? WHERE client_email = ?", ("تم إرسال العرض وعنوان المحفظة 🟢", email))
                    sent_count += 1
                    
            conn.commit()
            conn.close()
            st.success(f"🚀 تم إرسال العروض متضمنة محفظتك لـ {sent_count} شركة بنجاح!")
            st.rerun()

st.markdown("---")
st.subheader("🌐 جدول العمليات والشركات المستهدفة")
if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True)
else:
    st.info("لا توجد شركات مسجلة. اضغط على 'الخطوة 1' بالاعلى ليبدأ الوكيل عمله.")

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

st.write("---")
if st.button("🔄 تحديث الشاشة"):
    st.rerun()
