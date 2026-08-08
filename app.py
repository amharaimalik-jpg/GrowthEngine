import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Growth Engine - Fully Autonomous Agent",
    page_icon="⚡",
    layout="wide",
)

DB_NAME = "fully_autonomous_engine.db"

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
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        initial_companies = [
            ("TechNova Solutions", "info@technovasolutions.com", 2000.0, "lead", "بانتظار التشغيل الآلي", str(datetime.now().date())),
            ("PixelArt Digital Agency", "contact@pixelartagency.com", 2000.0, "lead", "بانتظار التشغيل الآلي", str(datetime.now().date())),
            ("GlobalSoft Tech", "support@globalsofttech.com", 2000.0, "lead", "بانتظار التشغيل الآلي", str(datetime.now().date()))
        ]
        cursor.executemany(
            "INSERT INTO sales (client_name, client_email, amount, status, outreach_status, last_contact_date) VALUES (?, ?, ?, ?, ?, ?)",
            initial_companies
        )
        conn.commit()
    conn.close()

init_db()

# --- الشريط الجانبي للإعدادات التلقائية ---
with st.sidebar:
    st.header("⚙️ إعدادات الوكيل الذاتي")
    secret_key = ""
    try:
        secret_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        pass
        
    gemini_key_input = st.text_input("مفتاح Gemini API Key:", value=secret_key, type="password")
    
    st.markdown("---")
    st.subheader("إعدادات بريد الإرسال (Gmail)")
    my_email_input = st.text_input("بريدك الإلكتروني:", value="amharaimalik@gmail.com")
    my_pass_input = st.text_input("كلمة مرور التطبيق:", type="password", value="malik@kilam/1234$4321")

    st.markdown("---")
    st.subheader("💳 ربط بوابة الدفع (Stripe)")
    stripe_link_input = st.text_input("رابط الدفع المباشر:", value="https://buy.stripe.com/test_your_link_here")

def call_gemini_bulletproof(prompt_text, api_key):
    if not api_key:
        return "⚠️ تنبيه: يرجى إدخال مفتاح Gemini API Key."
    
    urls = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    ]
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                if "candidates" in res_json and len(res_json["candidates"]) > 0:
                    parts = res_json["candidates"][0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"]
        except Exception:
            continue
            
    return "عزيزي العميل، نظامنا الذاتي يقدم لك فرصة حصرية لمضاعفة الأرباح. تفضل بالاطلاع وإتمام الدفع عبر الرابط المرفق."

def send_autonomous_email_to_client(target_email, subject, ai_message, sender_email, sender_password, stripe_link):
    if not sender_email or not sender_password:
        return False, "خطأ في بيانات البريد"

    full_message = f"{ai_message}\n\n-----------------------------------\nلإتمام التعاقد وبدء العمل فوراً، يرجى إتمام الدفع الآمن عبر الرابط التالي:\n{stripe_link}"

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
        return True, "تم الإرسال بنجاح"
    except Exception as e:
        return False, str(e)

st.title("⚡ Growth Engine - الوكيل الذاتي بالكامل (Autonomous Mode)")
st.success("🟢 النظام الآن في وضع التشغيل التلقائي الكامل.. اضغط الزر أدناه ودع الوكيل يتولى كل شيء!")

def get_data():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT client_name, client_email, amount, status, outreach_status, last_contact_date FROM sales")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "client_name": r[0],
            "client_email": r[1],
            "amount": r[2],
            "status": r[3],
            "outreach_status": r[4],
            "last_contact_date": r[5]
        }
        for r in rows
    ]

data = get_data()
closed_deals = [i for i in data if str(i.get("status")).lower() == "paid"]
total_earnings = sum(float(i.get("amount", 0)) for i in closed_deals)

c1, c2, c3, c4 = st.columns(4)
c1.metric("الشركات المرصودة", f"{len(data)} شركة")
c2.metric("حالة الوكيل الذاتي", "نشط ويعمل تلقائياً 🚀")
c3.metric("العقود المحصلة", f"{len(closed_deals)} عقد")
c4.metric("إجمالي الأرباح الفعلية", f"${total_earnings:,.2f} USD")

st.markdown("---")

# --- محرك التشغيل التلقائي الشامل (زر واحد لكل شيء) ---
st.subheader("🤖 لوحة القيادة الذاتية (أنت متفرج والوكيل ينفذ)")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🚀 تشغيل الطيار الآلي بالكامل (إرسال العروض للجميع تلقائياً)", type="primary"):
        if not gemini_key_input:
            st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
        else:
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT client_name, client_email FROM sales WHERE status != 'paid'")
            unpaid_leads = cursor.fetchall()
            
            success_count = 0
            for name, email in unpaid_leads:
                # صياغة الرسالة تلقائياً بالذكاء الاصطناعي
                ai_prompt = f"صمم رسالة إيميل تسويقية احترافية لشركة {name} لعرض نظام Autonomous Growth System بقيمة 2000 دولار."
                ai_msg = call_gemini_bulletproof(ai_prompt, gemini_key_input)
                
                # إرسال الإيميل تلقائياً
                sent, _ = send_autonomous_email_to_client(
                    target_email=email,
                    subject=f"فرصة نمو استراتيجية لشركة {name}",
                    ai_message=ai_msg,
                    sender_email=my_email_input,
                    sender_password=my_pass_input,
                    stripe_link=stripe_link_input
                )
                
                if sent:
                    cursor.execute("UPDATE sales SET outreach_status = ? WHERE client_name = ?", ("تم الإرسال آلياً بنجاح 🟢", name))
                    success_count += 1
            
            conn.commit()
            conn.close()
            st.success(f"🎉 قام الوكيل الآلي بإرسال العروض بنجاح إلى {success_count} شركة دون أي تدخل منك!")
            st.rerun()

with col_btn2:
    if st.button("💰 تفعيل محاكاة الدفع والتحصيل التلقائي للصفقات"):
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("UPDATE sales SET status = ?, outreach_status = ? WHERE status != 'paid'", 
                       ("paid", "تم التحصيل الآلي للأرباح 🟢"))
        conn.commit()
        conn.close()
        st.success("🎉 تم تحصيل إيرادات كافة الصفقات وتحديث الأرباح تلقائياً في النظام!")
        st.rerun()

st.write("---")

tab1, tab2 = st.tabs(["🌐 جدول العمليات المباشر", "✨ إضافة عملاء جدد آلياً"])

with tab1:
    st.subheader("🌐 جدول الشركات والعملاء وحالتهم مع الوكيل")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("لا توجد بيانات حالياً.")

with tab2:
    st.subheader("✨ توليد عملاء جدد تلقائياً للنظام")
    if st.button("➕ جلب دفعة شركات جديدة لقائمة الانتظار"):
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        cursor = conn.cursor()
        batch_leads = [
            ("Alpha Digital Hub", "partners@alphadigital.io", 2000.0, "lead", "تم الرصد الآلي", str(datetime.now().date())),
            ("Quantum Tech Labs", "contact@quantumlabs.tech", 2000.0, "lead", "تم الرصد الآلي", str(datetime.now().date()))
        ]
        cursor.executemany("INSERT INTO sales (client_name, client_email, amount, status, outreach_status, last_contact_date) VALUES (?, ?, ?, ?, ?, ?)", batch_leads)
        conn.commit()
        conn.close()
        st.success("🚀 تم إضافة عملاء جدد للقائمة بنجاح!")
        st.rerun()

st.write("---")
if st.button("🔄 تحديث الشاشة يدويّاً"):
    st.rerun()
