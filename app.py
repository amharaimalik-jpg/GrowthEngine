import time
import sqlite3
import threading
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import stripe
import google.generativeai as genai
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Growth Engine - Ultra Autonomous System",
    page_icon="⚡",
    layout="wide",
)

try:
    stripe.api_key = str(st.secrets.get("STRIPE_LIVE_KEY", "")).strip()
    raw_google_keys = str(st.secrets.get("GOOGLE_API_KEY", "")).strip()
    GOOGLE_API_KEYS = [k.strip() for k in raw_google_keys.split(",") if k.strip()]
    SEARCH_ENGINE_ID = str(st.secrets.get("SEARCH_ENGINE_ID", "")).strip()
except Exception:
    stripe.api_key = ""
    GOOGLE_API_KEYS = []
    SEARCH_ENGINE_ID = ""

gemini_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
if gemini_key:
    genai.configure(api_key=gemini_key)

DB_NAME = "autonomous_bot_pro.db"

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
            ("TechNova Solutions", "info@technovasolutions.com", 2000.0, "lead", "تم الرصد.. بانتظار التفاوض", str(datetime.now().date())),
            ("PixelArt Digital Agency", "contact@pixelartagency.com", 2000.0, "lead", "تم الرصد.. بانتظار التفاوض", str(datetime.now().date())),
            ("GlobalSoft Tech", "support@globalsofttech.com", 2000.0, "lead", "تم الرصد.. بانتظار التفاوض", str(datetime.now().date()))
        ]
        cursor.executemany(
            "INSERT INTO sales (client_name, client_email, amount, status, outreach_status, last_contact_date) VALUES (?, ?, ?, ?, ?, ?)",
            initial_companies
        )
        conn.commit()
    conn.close()

init_db()

def send_autonomous_email(target_email, subject, ai_message):
    sender_email = str(st.secrets.get("MY_EMAIL", "")).strip()
    sender_password = str(st.secrets.get("MY_EMAIL_PASSWORD", "")).strip()
    
    if not sender_email or not sender_password:
        return "⚠️ خطأ: لم يتم إعداد إيميلك أو كلمة مرور التطبيقات في الأسرار (Secrets)."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(ai_message, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return "✅ تم إرسال العرض بنجاح عبر الوكيل الآلي!"
    except Exception as e:
        return f"❌ فشل الإرسال: {e}"

st.title("⚡ Growth Engine Pro - النظام الذاتي لإدارة الصفقات والمبيعات")
st.success("🟢 النظام يعمل مجاناً بكامل طاقته عبر ذكاء Gemini الاصطناعي!")

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
c1.metric("الشركات المكتشفة", f"{len(data)} شركة")
c2.metric("حالة الروبوت", "يعمل 24/7 🚀")
c3.metric("الصفقات المغلقة", f"{len(closed_deals)} صفقة")
c4.metric("إجمالي الأرباح", f"${total_earnings:,.2f} USD")

st.write("---")

tab1, tab2, tab3 = st.tabs(["🌐 رادار الشركات والتحليلات", "🤖 وكيل المبيعات الذكي (Gemini AIDA)", "💳 بوابة تحصيل الأرباح"])

with tab1:
    st.subheader("🌐 جدول العمليات الحية وقاعدة بيانات الصفقات")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("⏳ جاري جلب الشركات الأولى..")

with tab2:
    st.subheader("💬 وكيل المبيعات الذكي المجاني (Gemini)")
    
    if data:
        company_options = [row["client_name"] for row in data]
        selected_company = st.selectbox("اختر الشركة المستهدفة للتفاوض:", company_options)
        
        selected_row = next((r for r in data if r["client_name"] == selected_company), None)
        default_email = selected_row["client_email"] if selected_row else ""
    else:
        selected_company = "شركة افتراضية"
        default_email = ""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    pain_point = st.text_input("💡 حدد نقطة ألم العميل أو أمر خاص للوكيل:", "ركز على مضاعفة المبيعات وتوفير الوقت")

    if prompt := st.chat_input("اطلب من الوكيل صياغة الرد أو العرض..."):
        full_user_prompt = f"الهدف: {prompt} | نقطة الألم المستهدفة: {pain_point}"
        st.session_state.messages.append({"role": "user", "content": full_user_prompt})
        with st.chat_message("user"):
            st.markdown(full_user_prompt)

        with st.chat_message("assistant"):
            if gemini_key:
                full_query = f"""أنت مدير مبيعات خبير وعالمي. العميل المستهدف: {selected_company}.
                خدمتنا هي 'Autonomous Growth System' بقيمة 2000 دولار.
                صيغ رسالة بريد إلكتروني احترافية جداً مستخدماً استراتيجية (AIDA: Attention, Interest, Desire, Action) بناءً على طلب المستخدم التالي: {full_user_prompt}
                اكتب نص الإيميل التسويقي فقط دون شروحات جانبية."""
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(full_query)
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"خطأ في الاتصال بـ Gemini: {e}"
            else:
                ai_response = "يرجى إضافة مفتاح GEMINI_API_KEY في الأسرار."

            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

    st.write("---")
    st.markdown("### 🚀 الإرسال الآلي والتعديل البشري الذكي")
    target_client_email = st.text_input("إيميل العميل المستهدف للإرسال:", value=default_email)
    
    if st.button("🚀 تفويض الوكيل بإرسال الإيميل وتسجيل المتابعة"):
        assistant_messages = [m["content"] for m in st.session_state.messages if m["role"] == "assistant"]
        if not assistant_messages:
            st.warning("⚠️ لا توجد رسالة مُصاغة! اطلب من الوكيل كتابة العرض أولاً.")
        elif not target_client_email:
            st.warning("⚠️ الرجاء إدخال إيميل العميل.")
        else:
            with st.spinner("الوكيل يقوم بإرسال الإيميل وتسجيل تاريخ المتابعة..."):
                last_ai_message = assistant_messages[-1]
                result = send_autonomous_email(
                    target_email=target_client_email,
                    subject=f"فرصة نمو استراتيجية لشركة {selected_company}",
                    ai_message=last_ai_message
                )
                if "✅" in result:
                    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE sales SET outreach_status = ?, last_contact_date = ? WHERE client_name = ?", 
                                   ("تم الإرسال وبانتظار المتابعة", str(datetime.now().date()), selected_company))
                    conn.commit()
                    conn.close()
                    st.success(result + " وتم تسجيل تاريخ المتابعة في النظام بنجاح!")
                else:
                    st.error(result)

with tab3:
    st.subheader("💳 بوابة تحصيل الأرباح")
    st.info("💡 بما أنك لا تمتلك حساباً بنكياً حالياً، يمكنك ترك بوابة Stripe معطلة.")

st.write("---")
if st.button("🔄 تحديث الشاشة يدويّاً"):
    st.rerun()
