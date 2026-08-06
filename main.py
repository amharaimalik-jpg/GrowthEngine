# main.py
import offer_config
import scraper
import outreach
import payment_gateway
import db_manager
import datetime
import os

def main_menu():
    while True:
        print("\n" + "="*50)
        print("🚀 GrowthEngine Master Control Center (SQLite Architecture)")
        print("="*50)
        print("1. Run Full Pipeline (Scrape -> Outreach -> Collect)")
        print("2. Search & Query Database")
        print("3. Financial Analytics & Reports")
        print("4. Export Executive Report")
        print("5. Exit System")
        print("="*50)
        
        choice = input("Enter your choice (1 to 5): ").strip()
        
        if choice == '1':
            print("\n--- Running Full Pipeline ---")
            print(offer_config.get_offer_summary())
            print("\n[Step 1] Generating Target Leads & Saving to SQLite Database...")
            scraper.generate_target_leads()
            
            print("\n[Step 2] Launching Outbound Campaign...")
            outreach.launch_outbound_campaign()
            
            print("\n[Step 3] Processing Payments via Gateway & Updating Database...")
            payment_gateway.process_incoming_payments()
            print("\n--- 🌟 Full Pipeline Completed Successfully! Database Updated! ---\n")
            
        elif choice == '2':
            print("\n--- Search & Query SQLite Database ---")
            rows = db_manager.get_all_leads()
            if rows:
                print(f"{'ID':<5} | {'Name':<30} | {'Email':<30} | {'Niche':<25} | {'Status':<10}")
                print("-" * 105)
                for row in rows:
                    print(f"{row[0]:<5} | {row[1]:<30} | {row[2]:<30} | {row[3]:<25} | {row[4]:<10}")
            else:
                print("[-] Database is empty. Run Full Pipeline first.")
                
        elif choice == '3':
            print("\n--- Calculating Financial Analytics ---")
            rows = db_manager.get_all_leads()
            if rows:
                total_clients = len(rows)
                paid_clients = sum(1 for r in rows if r[4] == 'Paid')
                revenue = paid_clients * 2000
                pipeline = total_clients * 2000
                print(f"📊 Total Clients in DB: {total_clients}")
                print(f"🔥 Active/Paid Clients: {paid_clients}")
                print(f"💰 Pipeline Value: ${pipeline:,}")
                print(f"💎 Successful Revenue: ${revenue:,}")
            else:
                print("[-] No data found in database.")
                
        elif choice == '4':
            print("\n--- Exporting Executive Report from Database ---")
            rows = db_manager.get_all_leads()
            if rows:
                filename = f"Executive_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Name', 'Email', 'Niche', 'Status'])
                    writer.writerows(rows)
                print(f"[+] Executive Report exported successfully as: {filename}")
            else:
                print("[-] No database records to export.")
                
        elif choice == '5':
            print("Exiting System. Goodbye, Emperor!")
            break
        else:
            print("[-] Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()