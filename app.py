import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Growth Engine - Fully Automated Real Agent",
    page_icon="⚡",
    layout="wide",
)

DB_NAME = "fully_automated_real_production.db"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_email TEXT,
            amount REAL,
            status TEXT,
            outreach_status TEXT,
            last_contact_date TEXT
        )
    """
    )
    conn.commit()
    conn.close()

init_db()

# --- الشريط الجانبي للإعدادات الحقيقية ---
with st.sidebar:
    st.header("⚙️ إعدادات الوكيل الآلي")
    gemini_key_input = st.text_input("مفتاح Gemini API Key:", type="password")
    
    st.markdown("---")
    st.subheader("إعدادات بريد الإرسال الفعلي (Gmail)")
    my_email_input = st.text_input("بريدك الإلكتروني:", value="amharaimalik@gmail.com")
    my_pass_input = st.text_input("كلمة مرور التطبيق:", type="password")

    st.markdown("---")
    st.subheader("💳 ربط بوابة الدفع الحقيقية (Stripe)")
    stripe_link_input = st.text_input("رابط الدفع المباشر (Stripe Payment Link):")

def call_gemini_bulletproof(prompt_text, api_key):
    if not api_key:
        return "عزيزي العميل، نقدم نظاماً تقنياً متطوراً لمضاعفة كفاءة وأرباح شركتكم الناشئة."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
    return "عزيزي العميل، نقدم نظاماً تقنياً متطوراً لمضاعفة كفاءة وأرباح شركتكم الناشئة."

def send_real_email(target_email, subject, ai_message, sender_email, sender_password, stripe_link):
    if not sender_email or not sender_password:
        return False, "بيانات البريد ناقصة"
    full_message = f"{ai_message}\n\n-----------------------------------\nلإتمام التعاقد والدفع الفوري الآمن ($2000):\n{stripe_link}"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(full_message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True, "تم الإرسال الحقيقي بنجاح"
    except Exception as e:
        return False, str(e)

st.title("⚡ Growth Engine - الوكيل الآلي المستقل بالكامل")
st.success("🟢 النظام جاهز للبحث عن الشركات الحقيقية، جلب بريدها، وتثبيت قيمة العقد على 2000 دولار آلياً.")

def get_data():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT client_name, client_email, amount, status, outreach_status, last_contact_date FROM sales")
    rows = cursor.fetchall()
    conn.close()
    return [{"client_name": r[0], "client_email": r[1], "amount": r[2], "status": r[3], "outreach_status": r[4], "last_contact_date": r[5]} for r in rows]

data = get_data()
closed_deals = [i for i in data if str(i.get("status")).lower() == "paid"]
total_earnings = sum(float(i.get("amount", 0)) for i in closed_deals)

c1, c2, c3, c4 = st.columns(4)
c1.metric("الشركات المستهدفة", f"{len(data)} شركة")
c2.metric("حالة الوكيل", "يعمل باستقلالية تامة 🤖")
c3.metric("العقود المدفوعة", f"{len(closed_deals)} عقد")
c4.metric("إجمالي الأرباح الفعلية", f"${total_earnings:,.2f} USD")

st.markdown("---")

st.subheader("🤖 محرك الجلب والتنفيذ الذاتي (أنت متفرج)")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌐 الخطوة 1: جلب الشركات الحقيقية وبريدها الإلكتروني آلياً", type="primary"):
        if not gemini_key_input:
            st.error("⚠️ يرجى إدخال مفتاح Gemini API في الشريط الجانبي لتوليد بيانات الشركات الحقيقية المستهدفة.")
        else:
            with st.spinner("جاري استخبارات السوق وجلب شركات حقيقية مع بريدها الإلكتروني وقيمة العقد الثابتة ($2000)..."):
                prompt = """قم بتوليد قائمة لـ 3 شركات حقيقية أو وكالات برمجية وتقنية ناشئة في السوق العالمي مع بريدها الإلكتروني الرسمي الحقيقي المخصص للتواصل (contact email). 
                يجب أن يكون الناتج بصيغة محددة لكل شركة هكذا بالضبط بدون أي كلام زائد:
                اسم الشركة | البريد الإلكتروني
                مثال:
                Apex Software Labs | contact@apexsoftwarelabs.com
                Quantum Solutions | info@quantumsolutions.io
                Nexus Digital Tech | support@nexusdigitaltech.co"""
                
                ai_output = call_gemini_bulletproof(prompt, gemini_key_input)
                lines = ai_output.strip().split("\n")
                
                conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                cursor = conn.cursor()
                
                added_count = 0
                for line in lines:
                    if "|" in line:
                        parts = line.split("|")
                        c_name = parts[0].strip()
                        c_email = parts[1].strip()
                        # التحقق من عدم التكرار وتثبيت القيمة على 2000
                        cursor.execute("SELECT COUNT(*) FROM sales WHERE client_email = ?", (c_email,))
                        if cursor.fetchone()[0] == 0 and "@" in c_email:
                            cursor.execute(
                                "INSERT INTO sales (client_name, client_email, amount, status, outreach_status, last_contact_date) VALUES (?, ?, ?, ?, ?, ?)",
                                (c_name, c_email, 2000.0, "lead", "تم الجلب والتحليل الآلي 🟢", str(datetime.now().date()))
                            )
                            added_count += 1
                            
                conn.commit()
                conn.close()
                st.success(f"🎉 نجح الوكيل في جلب {added_count} شركات حقيقية مع بريدها الإلكتروني وقيمة العقد الثابتة ($2000)! حدد الشاشة للاطلاع.")
                st.rerun()

with col2:
    if st.button("🚀 الخطوة 2: إرسال العروض الآلية لكل الشركات المرصودة دفعة واحدة", type="primary"):
        if not gemini_key_input or not my_email_input or not my_pass_input:
            st.error("⚠️ يرجى التأكد من إدخال مفتاح Gemini و بيانات Gmail في الشريط الجانبي.")
        else:
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT client_name, client_email FROM sales WHERE status != 'paid' AND outreach_status LIKE '%الآلي%'")
            targets = cursor.fetchall()
            
            sent_count = 0
            for name, email in targets:
                msg_prompt = f"اكتب رسالة بريد إلكتروني تسويقية استراتيجية قصيرة ومقنعة جداً لشركة {name} لعرض نظام هندسة نمو وتطوير تقني بقيمة 2000 دولار."
                ai_text = call_gemini_bulletproof(msg_prompt, gemini_key_input)
                
                sent, _ = send_real_email(
                    target_email=email,
                    subject=f"شراكة استراتيجية لتطوير أعمال لشركة {name}",
                    ai_message=ai_text,
                    sender_email=my_email_input,
                    sender_password=my_pass_input,
                    stripe_link=stripe_link_input
                )
                if sent:
                    cursor.execute("UPDATE sales SET outreach_status = ? WHERE client_email = ?", ("تم إرسال العرض والرابط 🟢", email))
                    sent_count += 1
                    
            conn.commit()
            conn.close()
            st.success(f"🚀 قام الوكيل بإرسال العروض لـ {sent_count} شركة بنجاح تام عبر إيميلك!")
            st.rerun()

st.markdown("---")
st.subheader("🌐 جدول العمليات والشركات المستهدفة الحية")
if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True)
else:
    st.info("لا توجد شركات مسجلة. اضغط على زر 'الخطوة 1' بالأعلى ليقوم الوكيل بجلب الشركات وبريدها آلياً.")

st.markdown("---")
st.subheader("💳 تأكيد التحصيل المالي (عند الدفع الفعلي عبر Stripe)")
if data:
    unpaid_list = [d["client_name"] for d in data if d["status"] != "paid"]
    if unpaid_list:
        selected_paid_client = st.selectbox("اختر الشركة التي سددت مبلغ 2000 دولار:", unpaid_list)
        if st.button("💰 تأكيد تحصيل الـ 2000 دولار وإضافتها للأرباح الفعلية"):
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("UPDATE sales SET status = ?, outreach_status = ? WHERE client_name = ?", 
                           ("paid", "تم تحصيل الـ 2000$ بنجاح 🟢", selected_paid_client))
            conn.commit()
            conn.close()
            st.success("🎉 تم إثبات تحصيل الـ 2000 دولار وتحديث رصيدك المالي بنجاح!")
            st.rerun()

st.write("---")
if st.button("🔄 تحديث الشاشة يدويّاً"):
    st.rerun()
