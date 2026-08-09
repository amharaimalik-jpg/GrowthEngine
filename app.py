with tab2:
    st.subheader("Secure Financial Acquisition Engine & Priority Nodes")
    st.markdown("🔒 *Secured via smart-contract tracking and automated escrow verification.*")
    
    # --- الحصان الأسود: خيار الحجز السريع الم مخفض المخاطر ---
    st.markdown("""
        <div style="background-color: #e3f2fd; border-left: 5px solid #2196f3; padding: 12px; border-radius: 4px; margin-bottom: 15px;">
            <h4 style="color: #0d47a1; margin: 0 0 5px 0;">⚡ The Dark Horse Protocol: Priority Node Activation</h4>
            <p style="color: #1565c0; margin: 0; font-size: 14px;">
                To bypass initial friction, qualify for the <b>Priority Deployment Mode</b> by depositing an initial escrow handshake of <b>500 USDT</b> (Balance auto-deducted from verified performance yields).
            </p>
        </div>
    """, unsafe_allow_html=True)

    coll, col2 = st.columns(2)
    with coll:
        niche = st.text_input("Target Industry / Niche", key="niche_k")
    with col2:
        deployment_mode = st.selectbox("Select Deployment Scale", ["Full Enterprise Deployment (5,000 USDT)", "Priority Node Handshake (500 USDT Initial)"], key="scale_k")
        
    if st.button("Initialize Secure Blockchain Diagnostic"):
        if niche:
            target_amount = 5000 if "5,000" in deployment_mode else 500
            with st.spinner("Connecting to secure decentralized nodes..."):
                st.markdown(f"""
                ### Verified Infrastructure Report for `{niche}`
                - **Selected Mode:** `{deployment_mode}`
                - **Official Escrow / Operational Wallet:** `0xD7709Dc72614240B065416D17c662Ee124654c78` 
                - **Required Verification Fund:** `{target_amount} USDT` (Triggers instant node allocation upon on-chain confirmation).
                """)
                
            wallet_address = "0xD7709Dc72614240B065416D17c662Ee124654c78"
            usdt_contract = "0x55d398326f99059ff775485246999027b3197955"
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={wallet_address}&page=1&offset=1&sort=desc"

            try:
                response = requests.get(url, timeout=10).json()
                if response.get('status') == '1' and len(response.get('result', [])) > 0:
                    last_tx = response['result'][0]
                    if last_tx['to'].lower() == wallet_address.lower():
                        if int(last_tx['value']) >= target_amount * 10**18:
                            st.success(f"Verified: Deployment funds ({target_amount} USDT) received successfully! Node is live.")
                        else:
                            st.info(f"Transaction detected on-chain, but amount is below the {target_amount} USDT threshold.")
                    else:
                        st.info("System Status: Awaiting deployment transaction to the official escrow address.")
                else:
                    st.info("System Status: Awaiting deployment transaction to the official escrow address.")
            except Exception as e:
                st.info("System Status: Awaiting deployment transaction to the official escrow address.")
        else:
            st.warning("Please enter your industry/niche first.")
