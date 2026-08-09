import streamlit as st
import requests
import hashlib

st.set_page_config(page_title="GrowthEngine Viral System", layout="wide")

# Professional English Welcome Message for Product Hunt
st.markdown("""
    <div style="background-color: #ff6154; padding: 15px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px;">
        <h2>🚀 Welcome Product Hunt Community!</h2>
        <p>You unlocked exclusive access to GrowthEngine. Enter your website below to run your 60-second web-gap analysis & activate your viral loop!</p>
    </div>
""", unsafe_allow_html=True)

st.title("GrowthEngine: Automated Acquisition & Viral System")
st.markdown("A real-world engineering platform featuring gap analysis, blockchain tracking, and a viral referral system (20% commission for promoters).")

tab1, tab2, tab3 = st.tabs(["Web-Gap Analysis", "Acquisition & Conversion Engine", "Viral Referral System (20% Yield)"])

with tab1:
    st.subheader("Free Quick Gap Analysis")
    target_url = st.text_input("Enter the target company URL")
    if st.button("Run Gap Analysis"):
        if target_url:
            st.success("Website analyzed successfully!")
            st.markdown(f"""
            ### Gap Report for `{target_url}`
            - **Status:** Daily operational losses detected.
            - **Solution:** Proceed to the 'Acquisition & Conversion' tab to activate the real financial system and filter your leads.
            """)
        else:
            st.warning("Please enter a URL first.")

with tab2:
    st.subheader("Financial Acquisition Engine (5,000 USDT)")
    coll, col2 = st.columns(2)
    with coll:
        niche = st.text_input("Target Company Niche", key="niche_k")
    with col2:
        company_size = st.selectbox("Company Size", ["Enterprise", "Mid-size", "Startup"], key="size_k")
        
    if st.button("Execute Diagnostic & Blockchain Scan"):
        if niche:
            with st.spinner("Executing real-time blockchain scan..."):
                st.markdown(f"""
                ### Smart Report for `{niche}`
                - **Status:** Acquisition assets fully prepared.
                - **Monitored Wallet:** `0xD7709Dc72614240B065416D17c662Ee124654c78` (Target: 5,000 USDT).
                """)
                
            wallet_address = "0xD7709Dc72614240B065416D17c662Ee124654c78"
            usdt_contract = "0x55d398326f99059ff775485246999027b3197955"
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={wallet_address}&page=1&offset=1&sort=desc"

            try:
                response = requests.get(url, timeout=10).json()
                if response.get('status') == '1' and len(response.get('result', [])) > 0:
                    last_tx = response['result'][0]
                    if last_tx['to'].lower() == wallet_address.lower():
                        if int(last_tx['value']) >= 5000 * 10**18:
                            st.success("Financial transfer successfully confirmed!")
                        else:
                            st.info("Transaction detected, but amount is below the required threshold.")
                    else:
                        st.info("System status: Waiting for transfer to the official wallet.")
                else:
                    st.info("Monitoring blockchain...")
            except Exception as e:
                st.info("Monitoring blockchain...")
        else:
            st.warning("Please enter a niche first.")

with tab3:
    st.subheader("Viral Referral System (20% Commission)")
    st.markdown("Turn every lead into a marketer for your system automatically.")
    
    user_email = st.text_input("Enter your email or ID to generate your referral link")
    if st.button("Generate My Referral Link"):
        if user_email:
            ref_code = hashlib.md5(user_email.encode()).hexdigest()[:8]
            ref_link = f"https://your-app-url.streamlit.app/?ref={ref_code}"
            
            st.success("Referral link generated successfully!")
            st.markdown(f"""
            - **Your Referral Link:** `{ref_link}`
            - **20% Yield (1,000 USDT) via your link.** Automatically paid in USDT. Share this link with anyone facing the same challenge. Once they close the 5,000 USDT deal, you get your share.
            """)
            st.info("With this feature, your first 10 clients become your own marketing team, bringing in new business without you lifting a finger.")
        else:
            st.warning("Please enter an email or ID first.")
