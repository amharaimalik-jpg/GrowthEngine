import sqlite3
import pandas as pd

def get_leads_for_outreach(min_score_threshold=80):
    """استخراج المتاجر التي تعاني من مشاكل في الأداء (تقييم أقل من 80)"""
    conn = sqlite3.connect("growth_data.db")
    
    query = """
    SELECT domain, score, latency, audit_url 
    FROM audits 
    WHERE score < ? 
    ORDER BY score ASC
    """
    
    df = pd.read_sql_query(query, conn, params=(min_score_threshold,))
    conn.close()
    return df

def generate_outreach_campaign():
    leads = get_leads_for_outreach()
    print(f"🎯 Found {len(leads)} potential leads with performance issues.\n")
    
    campaign_data = []
    
    for idx, row in leads.iterrows():
        domain = row['domain']
        score = row['score']
        latency = row['latency']
        audit_link = row['audit_url']
        
        # صيغة الرسالة المؤثرة المستهدفة للعميل
        message = (
            f"Hello {domain} team,\n\n"
            f"We performed an automated health check on your store and detected a latency of {latency}s "
            f"with an overall performance score of {score}%.\n\n"
            f"You can view your live diagnostic report and performance fixes here:\n"
            f"{audit_link}\n\n"
            f"Best regards,\nGrowthEngine Automation"
        )
        
        campaign_data.append({
            "domain": domain,
            "score": score,
            "latency": latency,
            "audit_link": audit_link,
            "message_body": message
        })
        
    # حفظ الحملة في ملف CSV لتنفيذ الإرسال الجماعي
    campaign_df = pd.DataFrame(campaign_data)
    campaign_df.to_csv("outreach_campaign_leads.csv", index=False)
    print("✅ Outreach campaign generated successfully: 'outreach_campaign_leads.csv'")

if __name__ == "__main__":
    generate_outreach_campaign()
