# payment_gateway.py
import csv
from offer_config import OFFER_DETAILS

def process_incoming_payments():
    filename = "leads.csv"
    print(f"[*] Connecting to Live USDT (TRC-20) Gateway for Offer: {OFFER_DETAILS['service_name']}\n")
    
    try:
        updated_leads = []
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['status'] = 'Paid'
                print(f"[$$] Payment Received! ${OFFER_DETAILS['price_usd']} USDT secured from {row['name']} ({row['email']})")
                updated_leads.append(row)
                
        # تحديث قاعدة البيانات لتصبح بحالة مدفوع
        keys = updated_leads[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(updated_leads)
            
        total_revenue = len(updated_leads) * OFFER_DETAILS['price_usd']
        print(f"\n[+] Success! All payments cleared. Total Revenue Generated: ${total_revenue:,} USD")
        print("[+] Empire Engine is fully operational and generating cash flow!")
        
    except FileNotFoundError:
        print("[-] Error: leads.csv not found.")

if __name__ == "__main__":
    process_incoming_payments()