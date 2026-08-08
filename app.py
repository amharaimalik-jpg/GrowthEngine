import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Growth Engine - Ultimate Real Production",
    page_icon="⚡",
    layout="wide",
)

DB_NAME = "real_production_engine.db"

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

# --- الشريط الجانبي للإعدادات الحقيقية والإنتاجية ---
with st.sidebar:
    st.header("⚙️ إعدادات الإنتاج الحقيقي")
    gemini_key_input = st.text_input("مفتاح Gemini API Key:", type="password")
    
    st.markdown("---")
    st.subheader("إعدادات بريد الإرسال الفعلي (Gmail)")
    my_email_input = st.text_input("بريدك الإلكتروني:", value="amharaimalik@gmail.com")
    my_pass_input = st.text_input("كلمة مرور التطبيق:", type="password")

    st.markdown("---")
    st.subheader("💳 ربط بوابة الدفع الحقيقية (Stripe)")
    stripe_link_input = st.text_input("رابط الدفع المباشر (Stripe Payment Link):")
    
    st.markdown("---")
    st.subheader("🌐 ربط بيانات الشركات الحقيقية (Apollo / Google Places)")
    api_provider = st.selectbox("اختر مزود البيانات:", ["إدخال يدوي لشركة حقيقية", "بحث عبر API خارجي"])

def call_gemini_bulletproof(prompt_text, api_key):
    if not api_key:
        return "⚠️ يرجى إدخال مفتاح Gemini API."
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
    return "عزيزي العميل، نود عرض شراكة استراتيجية لتطوير أعمالكم."

def send_real_email(target_email, subject, ai_message, sender_email, sender_password, stripe_link):
    if not sender_email or not sender_password:
        return False, "بيانات البريد ناقصة"
    full_message = f"{ai_message}\n\n-----------------------------------\nلإتمام التعاقد والدفع الفوري الآمن:\n{stripe_link}"
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

st.title("⚡ Growth Engine - النظام الإنتاجي الحقيقي")
st.success("🟢 النظام جاهز للعمل الفعلي مع البريد وبوابة الدفع الحقيقية.")

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
c1.metric("الشركات الحقيقية المسجلة", f"{len(data)} شركة")
c2.metric("حالة النظام", "متصل للإنتاج 🌐")
c3.metric("العقود المدفوعة حقيقةً", f"{len(closed_deals)} عقد")
c4.metric("إجمالي الأرباح المستلمة فعلياً", f"${total_earnings:,.2f} USD")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🌐 إضافة شركة حقيقية وإدارتها", "🚀 نظام التواصل والإرسال الفعلي", "💳 تأكيد الأرباح والمدفوعات الحقيقية"])

with tab1:
    st.subheader("➕ إضافة شركة حقيقية جديدة للعمليات")
    with st.form("real_client_form"):
        r_name = st.text_input("اسم الشركة الحقيقية:")
        r_email = st.text_input("البريد الإلكتروني الحقيقي للشركة:")
        r_amount = st.number_input("قيمة الخدمة/العقد بالدولار:", value=2000.0)
        submit_real = st.form_submit_button("حفظ الشركة في قاعدة البيانات الحقيقية")
        if submit_real and r_name and r_email:
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sales (client_name, client_email, amount, status, outreach_status, last_contact_date) VALUES (?, ?, ?, ?, ?, ?)",
                           (r_name, r_email, r_amount, "lead", "جاهز للتواصل الفعلي", str(datetime.now().date())))
            conn.commit()
            conn.close()
            st.success("✅ تمت إضافة الشركة الحقيقية بنجاح!")
            st.rerun()

    st.markdown("### جدول العمليات الحالية")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("لا توجد شركات مسجلة حتى الآن. قم بإضافة شركة حقيقية بالأعلى.")

with tab2:
    st.subheader("🚀 إرسال العروض الحقيقية للشركات")
    if data:
        target_names = [d["client_name"] for d in data if d["status"] != "paid"]
        if target_names:
            selected_real_company = st.selectbox("اختر الشركة للإرسال الفعلي:", target_names)
            row_info = next((d for d in data if d["client_name"] == selected_real_company), None)
            
            if st.button("📤 توليد الإيميل الذكي وإرساله فعلياً للشركة"):
                if not gemini_key_input:
                    st.error("أدخل مفتاح Gemini API.")
                else:
                    prompt = f"اكتب إيميل احترافي لشركة {selected_real_company} لعرض نظام تقني متقدم بقيمة {row_info['amount']} دولار."
                    ai_text = call_gemini_bulletproof(prompt, gemini_key_input)
                    
                    sent, msg_res = send_real_email(
                        target_email=row_info["client_email"],
                        subject=f"فرصة تطوير استراتيجية لشركة {selected_real_company}",
                        ai_message=ai_text,
                        sender_email=my_email_input,
                        sender_password=my_pass_input,
                        stripe_link=stripe_link_input
                    )
                    
                    if sent:
                        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                        cursor = conn.cursor()
                        cursor.execute("UPDATE sales SET outreach_status = ? WHERE client_name = ?", ("تم الإرسال بنجاح 🟢", selected_real_company))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم إرسال الإيميل للشركة الحقيقية عبر خادم Gmail الخاص بك بنجاح!")
                    else:
                        st.error(f"❌ فشل الإرسال: {msg_res}")
        else:
            st.info("جميع الشركات الحالية أكملت الصفقات أو لا توجد شركات متاحة للإرسال.")

with tab3:
    st.subheader("💳 تأكيد الإيرادات والأرباح الحقيقية")
    st.write("بمجرد أن يدفع العميل عبر رابط Stripe وتتأكد من دخول المبلغ لحسابك البنكي أو لوحة تحكم Stripe، قم بتحديث حالتها هنا:")
    if data:
        paid_options = [d["client_name"] for d in data if d["status"] != "paid"]
        if paid_options:
            chosen_paid = st.selectbox("اختر الشركة التي سددت المبلغ الحقيقي:", paid_options)
            if st.button("💰 تأكيد استلام الأموال الحقيقية وتحديث الأرباح"):
                conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute("UPDATE sales SET status = ?, outreach_status = ? WHERE client_name = ?", 
                               ("paid", "تم الدفع والاستلام الحقيقي 🟢", chosen_paid))
                conn.commit()
                conn.close()
                st.success("🎉 تم تحديث رصيد الأرباح وإثبات العقد المدفوع بنجاح في النظام!")
                st.rerun()

st.write("---")
if st.button("🔄 تحديث البيانات"):
    st.rerun()
