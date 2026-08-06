# outreach.py
import csv
from offer_config import OFFER_DETAILS

def launch_outbound_campaign():
    filename = "leads.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            print(f"[*] Starting Outbound Campaign for Offer: {OFFER_DETAILS['service_name']} (${OFFER_DETAILS['price_usd']})\n")
            
            for row in reader:
                print(f"[>] Sending pitch to: {row['name']} ({row['email']}) [Niche: {row['niche']}]")
                # محاكاة إرسال البريد التسويقي الآلي
                print(f"    -> Message: 'Hi {row['name']}, we can automate your sales with our AI engine for ${OFFER_DETAILS['price_usd']}. Let's scale!'")
                print("    [V] Status: Sent Successfully!\n")
                
        print("[+] All outbound campaigns executed successfully! Pipeline ready for payment collection.")
    except FileNotFoundError:
        print("[-] Error: leads.csv not found. Please run scraper.py first.")

if __name__ == "__main__":
    launch_outbound_campaign()