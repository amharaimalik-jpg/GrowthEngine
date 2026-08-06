import pandas as pd

def process_leads():
    print("Reading leads from leads.csv...")
    df = pd.read_csv("leads.csv")
    
    # تصفية العملاء النشطين فقط (Active leads)
    active_leads = df[df["Status"] == "Active"]
    
    print("\nFiltered Active Leads:")
    print(active_leads)
    
    print("\nData processing pipeline completed successfully.")
    return active_leads

if __name__ == "__main__":
    process_leads()