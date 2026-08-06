import sqlite3
import pandas as pd

def generate_financial_report():
    print("=== GrowthEngine V3 - Financial & Pipeline Analytics ===")
    conn = sqlite3.connect('leads_database.db')
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()
    
    if df.empty:
        print("No data found in the database to analyze.")
        return
        
    total_value = 0
    active_value = 0
    
    # تنظيف وحساب القيم المالية
    for _, row in df.iterrows():
        try:
            val_str = str(row['value']).replace('$', '').replace(',', '').strip()
            val_int = int(val_str)
            total_value += val_int
            
            if row['status'] == 'Active':
                active_value += val_int
        except Exception:
            pass
            
    active_leads_count = len(df[df['status'] == 'Active'])
    
    print(f"\n📊 إجمالي عدد العملاء في الأرشيف: {len(df)}")
    print(f"🔥 عدد العملاء النشطين (Active): {active_leads_count}")
    print(f"💰 إجمالي قيمة الصفقات المحتملة: ${total_value:,}")
    print(f"💎 القيمة المالية للعملاء النشطين جاهزة للاستهداف: ${active_value:,}")
    print("=" * 60)

if __name__ == "__main__":
    generate_financial_report()