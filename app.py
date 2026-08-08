import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

st.set_page_config(
    page_title="Growth Engine - Ultra Autonomous System",
    page_icon="⚡",
    layout="wide",
)

# قراءة مفتاح API وإعداده بمكتبة جوجل الرسمية
try:
    gemini_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    if gemini_key:
        genai.configure(api_key=gemini_key)
except Exception:
    gemini_key = ""

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

# --- الاتصال الآمن والمضمون باستخدام مكتبة جوجل الرسمية ---
def call_gemini_official(prompt_text):
    if not gemini_key:
        return "⚠️ خطأ: لم يتم العثور على مفتاح GEMINI_API_KEY في الأسرار."
    
    # قائمة النماذج الأكثر مرونة ودعماً للمفاتيح المجانية
    models_to_test = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for m_name in models_to_test:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt_text)
            if response and response.text:
                return response.text
        except Exception:
            continue
            
    return "❌ عذراً، لم نتمكن من الاتصال بالنموذج. تأكد من صحة المفتاح في إعدادات Streamlit Secrets."

def send_autonomous_email(target_email, subject, ai_message):
    sender_email = str(st.secrets.get("MY_EMAIL", "")).strip()
    sender_password = str(st.secrets.get("MY_EMAIL_PASSWORD", "")).strip()
    
    if not sender_email or not sender_password:
        return "⚠️ خطأ: لم يتم إعداد البريد أو كلمة المرور في الأسرار."

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
st.success("🟢 النظام يعمل مجاناً 100% بكفاءة عالية وبالمكتبة الرسمية لجوجل!")

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
                full_query = f"""أنت مدير مبيعات خبير. العميل المستهدف: {selected_company}.
                خدمتنا هي 'Autonomous Growth System' بقيمة 2000 دولار.
                صيغ رسالة بريد إلكتروني احترافية مستخدماً استراتيجية (AIDA) بناءً على طلب المستخدم التالي: {full_user_prompt}
                اكتب نص الإيميل التسويقي فقط دون شروحات جانبية."""
                
                with st.spinner("جاري صياغة الرد الذكي..."):
                    ai_response = call_gemini_official(full_query)
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
            st.warning("⚠️ لا توجد رسالة مُصاغة!")
        elif not target_client_email:
            st.warning("⚠️ الرجاء إدخال إيميل العميل.")
        else:
            with st.spinner("الوكيل يقوم بالإرسال..."):
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
                    st.success(result)
                else:
                    st.error(result)

with tab3:
    st.subheader("💳 بوابة تحصيل الأرباح")
    st.info("💡 النظام يعمل بصورة كاملة ومجانية.")

st.write("---")
if st.button("🔄 تحديث الشاشة يدويّاً"):
    st.rerun()
