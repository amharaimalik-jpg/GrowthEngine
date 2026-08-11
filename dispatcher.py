import sqlite3
import requests
import json
import os

# إعدادات API لمنصة Brevo
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "YOUR_BREVO_API_KEY_HERE")
BREVO_URL = "https://api.brevo.com/v3/smtp/email"

def send_automated_outreach():
    # الاتصال بقاعدة البيانات واستخراج المتاجر التي تعاني من بطء في الأداء
    conn = sqlite3.connect("growth_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT domain, score, latency, audit_url, email 
        FROM audits 
        WHERE score < 80 AND (status IS NULL OR status != 'sent')
    """)
    leads = cursor.fetchall()

    if not leads:
        print("لا يوجد عملاء جدد بحاجة للتواصل الآن.")
        conn.close()
        return

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    for domain, score, latency, audit_url, email in leads:
        if not email or "@" not in email:
            continue

        # تجهيز الرسالة الديناميكية المخصصة لكل متجر
        payload = {
            "sender": {"name": "GrowthEngine Systems", "email": "audit@growthengine.auto"},
            "to": [{"email": email}],
            "subject": f"Automated Speed & Optimization Audit for {domain}",
            "htmlContent": f"""
                <h3>Performance Alert for {domain}</h3>
                <p>An automated performance audit detected optimization bottlenecks on your website:</p>
                <ul>
                    <li><b>Performance Score:</b> {score}/100</li>
                    <li><b>Response Latency:</b> {latency}s</li>
                </ul>
                <p>Review your full diagnostic report and instant resolution setup here:</p>
                <p><a href="{audit_url}" style="background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">View Diagnostic Report</a></p>
            """
        }

        response = requests.post(BREVO_URL, json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"تم إرسال التقرير بنجاح إلى: {email}")
            cursor.execute("UPDATE audits SET status = 'sent' WHERE domain = ?", (domain,))
        else:
            print(f"فشل الإرسال إلى {email}: {response.text}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    send_automated_outreach()
