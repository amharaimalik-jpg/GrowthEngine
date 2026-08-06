import pandas as pd

def simulate_outreach():
    print("Initializing automated outreach & appointment setting engine...")
    try:
        # قراءة ملف العملاء المصفين
        df = pd.read_csv("leads.csv")
        active_leads = df[df["Status"] == "Active"]
        
        print(f"Found {len(active_leads)} high-value active targets. Launching outreach...")
        
        # محاكاة إرسال رسائل التواصل وحجز المواعيد تلقائياً
        for index, row in active_leads.iterrows():
            print(f" [OUTREACH SUCCESS] Sent tailored pitch to -> {row['Lead_Name']} | Value: {row['Value']}")
            
        print("All automated outreach sequences completed successfully!")
    except Exception as e:
        print(f"Error in outreach engine: {e}")

if __name__ == "__main__":
    simulate_outreach()