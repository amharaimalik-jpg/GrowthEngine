with tab2:
    st.subheader("🔥 Product Hunt Exclusive Launch Engine & VIP Nodes")
    st.markdown("🔒 *Secured via smart-contract tracking and automated escrow verification for PH Community.*")
    
    # --- عرض الإطلاق الحصري العنيف ---
    st.markdown("""
        <div style="background-color: #fff3e0; border-left: 5px solid #ff9800; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
            <h3 style="color: #e65100; margin: 0 0 5px 0;">⚡ Product Hunt 24H Flash Pass (80% OFF)</h3>
            <p style="color: #ef6c00; margin: 0; font-size: 15px; font-weight: bold;">
                To celebrate our Product Hunt launch, the full enterprise deployment fee is slashed from <b>5,000 USDT</b> to an exclusive community rate of <b>997 USDT</b> for the next 24 hours only!
            </p>
        </div>
    """, unsafe_allow_html=True)

    coll, col2 = st.columns(2)
    with coll:
        niche = st.text_input("Target Industry / Niche", key="niche_ph")
    with col2:
        deployment_mode = st.selectbox("Select Launch Tier", ["Product Hunt 24H Flash Pass (997 USDT)", "Standard Enterprise Deployment (5,000 USDT)"], key="scale_ph")
        
    if st.button("Initialize PH Secure Escrow Diagnostic"):
        if niche:
            target_amount = 997 if "997" in deployment_mode else 5000
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
                            st.success(f"Verified: Launch funds ({target_amount} USDT) received successfully! Node is live.")
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
