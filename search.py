import sqlite3
import pandas as pd

def search_leads():
    print("=== GrowthEngine V3 - Database Search Engine ===")
    conn = sqlite3.connect('leads_database.db')
    
    while True:
        print("\nOptions:")
        print("1. View all stored leads")
        print("2. Filter by Active status")
        print("3. Exit search engine")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            df = pd.read_sql_query("SELECT * FROM leads", conn)
            print("\n--- All Stored Leads in Database ---")
            print(df)
            
        elif choice == '2':
            df = pd.read_sql_query("SELECT * FROM leads WHERE status = 'Active'", conn)
            print("\n--- Active Leads Only ---")
            print(df)
            
        elif choice == '3':
            print("Exiting search engine. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
    conn.close()

if __name__ == "__main__":
    search_leads()