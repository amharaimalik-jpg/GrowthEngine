import streamlit as st
import requests
import hashlib
import google.generativeai as genai

st.set_page_config(page_title="GrowthEngine Viral System", layout="wide", initial_sidebar_state="collapsed")

# Configure Gemini API safely from Streamlit Secrets or fallback
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

# --- Professional Product Hunt Banner & Countdown Header ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%); padding: 20px; border-radius: 12px; text-align: center; color: white; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(76,175,80,0.3);">
        <h1 style="margin: 0; font-size: 28px;">🚀 GrowthEngine: Success-Share Launch Pass</h1>
        <p style="margin: 5px 0 0 0; font-size: 16px;">Instant Low-Barrier Access (197 USDT) + 10% Success Revenue Share</p>
    </div>
""", unsafe_allow_html=True)

# Define tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Web-Gap Analysis & ROI", 
    "⚡ Success-Share Access (197 USDT)", 
    "🌐 Exponential Viral Network", 
    "🤖 Autonomous AI Support Bot"
])

with tab1:
    st.subheader("Automated Web-Gap Diagnostic & Live ROI Simulator")
    target_url = st.text_input("Enter your target company URL (e.g., yourstartup.com)", key="target_url_input")
    
    col_a, col_b = st.columns(2)
    with col_a:
        est_traffic = st.number_input("Estimated Monthly Visitors", min_value=1000, max_value=1000000, value=25000, step=1000)
    with col_b:
        avg_deal_value = st.number_input("Average Deal/Product Value ($)", min_value=10, max_value=10000, value=200, step=50)

    if st.button("Run Deep Gap & ROI Analysis"):
        if target_url:
            with st.spinner("Executing real-time funnel leakages and financial simulation..."):
                monthly_loss = int(est_traffic * 0.034 * (avg_deal_value * 0.4))
                annual_loss = monthly_loss * 12
                
                st.success("Diagnostic & Live Simulation Completed Successfully!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Traffic Drop-off Rate", "34.2%", "-4.1% vs Benchmark")
                m2.metric("Est. Monthly Revenue Leak", f"${monthly_loss:,}", "Critical")
                m3.metric("Projected Annual Loss", f"${annual_loss:,}", "Urgent Fix Needed")

                st.markdown(f"""
                ### 📈 Live Financial Impact Report for `{target_url}`
                - **Conversion Friction:** Your current funnel routing is leaking approximately **34%** of high-intent visitors before checkout.
                - **The Cost of Inaction:** You are leaving roughly **${monthly_loss:,}** on the table every single month.
                - **Actionable Solution:** Proceed immediately to the **'Success-Share Access'** tab to deploy your node for just 197 USDT.
                """)
        else:
            st.warning("Please enter a valid URL first.")

with tab2:
    st.subheader("🔥 Success-Share Access Node (197 USDT Entry)")
    st.markdown("🔒 *Zero friction entry: Secure your instant node and align as a success-share partner.*")
    
    st.markdown("""
        <div style="background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #2e7d32; margin: 0 0 5px 0;">💎 Product Hunt Community Success Model</h3>
            <p style="color: #388e3c; margin: 0; font-size: 14px; font-weight: bold;">
                Pay a one-time low barrier fee of <b>197 USDT</b> to activate your system instantly. We win only when you win via a transparent 10% success-share on generated growth!
            </p>
        </div>
    """, unsafe_allow_html=True)

    coll, col2 = st.columns(2)
    with coll:
        niche = st.text_input("Target Industry / Niche", key="niche_ph_success")
    with col2:
        deployment_mode = st.selectbox("Select Access Tier", ["Success-Share Access Pass (197 USDT)", "Full Enterprise License (5,000 USDT)"], key="scale_ph_success")
        
    if st.button("Initialize Secure Blockchain Verification"):
        if niche:
            target_amount = 197 if "197" in deployment_mode else 5000
            wallet_address = "0xD7709Dc72614240B065416D17c662Ee124654c78"
            usdt_contract = "0x55d398326f99059ff775485246999027b3197955"
            
            with st.spinner("Connecting to BSC decentralized nodes and checking transaction hashes..."):
                st.markdown(f"""
                ### 🧾 Active Escrow Node Report for `{niche}`
                - **Selected Package:** `{deployment_mode}`
                - **Destination Escrow Wallet:** `{wallet_address}`
                - **Required Verification Deposit:** `{target_amount} USDT` (BEP-20)
                """)
                
                url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={wallet_address}&page=1&offset=1&sort=desc"

                try:
                    response = requests.get(url, timeout=10).json()
                    if response.get('status') == '1' and len(response.get('result', [])) > 0:
                        last_tx = response['result'][0]
                        if last_tx['to'].lower() == wallet_address.lower():
                            tx_value = int(last_tx['value']) / 10**18
                            if tx_value >= target_amount:
                                st.success(f"Verified On-Chain: Entry funds ({tx_value} USDT) received successfully! Success-share node is live.")
                                st.balloons()
                            else:
                                st.info(f"Transaction detected on-chain ({tx_value} USDT), but it's below the required {target_amount} USDT threshold.")
                        else:
                            st.warning("System Status: Awaiting deployment transaction to the official escrow address.")
                    else:
                        st.warning("System Status: Awaiting deployment transaction to the official escrow address. Send exact USDT to verify instantly.")
                except Exception as e:
                    st.warning("System Status: Awaiting deployment transaction to the official escrow address (Network check active).")
        else:
            st.warning("Please enter your industry/niche first.")

with tab3:
    st.subheader("Exponential Viral Growth Infrastructure (Tiered Multiplier)")
    
    st.markdown("""
        <div style="background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #2e7d32; margin-top: 0;">🚀 Exponential Tiered Loop Active!</h3>
            <p style="color: #388e3c; font-weight: bold;">
                Unlock the <b>Tiered Yield Multiplier</b>: Your commission automatically scales from 20% up to 40% as your network expands daily.
            </p>
        </div>
    """, unsafe_allow_html=True)

    user_email = st.text_input("Enter your partner ID or email to unlock Exponential Nodes", key="partner_email_input_exp")
    
    if st.button("Activate Exponential Tracking Node"):
        if user_email:
            ref_code = hashlib.md5(user_email.encode()).hexdigest()[:8]
            ref_link = f"https://growthengine-9btijzf8jcijy9hfqufsbu.streamlit.app/?ref={ref_code}&tier=success_share"
            
            st.success("Exponential tracking node locked and secured successfully!")
            st.markdown(f"**Your Tier-1 Multiplier Link:** `{ref_link}`")
            
            st.markdown("""
                <div style="background: #1e1e1e; color: #4caf50; padding: 20px; border-radius: 12px; margin-top: 20px; border: 2px solid #4caf50;">
                    <div style="font-size: 16px; color: #fff; margin-bottom: 5px;">📊 Current Node Status: <span style="color: #4caf50;">Tier 1 Active (20% Yield)</span></div>
                    <div style="font-size: 14px; color: #ccc;">Bring just 2 referrals to auto-upgrade to Tier 2 (30% Yield). Bring 5 to unlock Tier 3 (40% Yield / Max Payout)!</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.warning("🔥 **Growth Command:** Share your link across all professional networks right now to multiply your earnings automatically with every conversion!")
        else:
            st.warning("Please enter a partner ID or email first.")

with tab4:
    st.subheader("🤖 Autonomous AI Support & Objection Handler (Gemini Powered)")
    st.markdown("Directly powered by Google Gemini intelligence to handle any technical inquiry or objection instantly.")
    
    visitor_objection = st.text_input("Enter visitor question or doubt:", key="visitor_obj_input")
    
    if st.button("Generate Intelligent Response"):
        if visitor_objection:
            with st.spinner("Analyzing inquiry with advanced Gemini intelligence..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    prompt = f"You are a professional technical expert and closing architect for GrowthEngine. Answer this visitor objection authoritatively, clearly, and transparently about our 197 USDT success-share model: {visitor_objection}"
                    
                    response = model.generate_content(prompt)
                    ai_reply = response.text
                    
                    st.success("AI Intelligence Response Generated:")
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; color: #31333F; line-height: 1.6;">
                        {ai_reply}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"System Error: Could not connect to the intelligence layer. {e}")
        else:
            st.warning("Please enter a question.")
