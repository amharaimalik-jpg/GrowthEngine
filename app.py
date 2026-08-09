with tab3:
    st.subheader("Exponential Viral Growth Infrastructure (Tiered Multiplier)")
    
    st.markdown("""
        <div style="background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #2e7d32; margin-top: 0;">🚀 Exponential Tiered Loop Active!</h3>
            <p style="color: #388e3c; font-weight: bold;">
                Unlock the <b>Tiered Yield Multiplier</b>: Your commission automatically scales from 20% up to 40% (2,000 USDT per referral) as your network expands daily. The more you bring, the higher your multiplier!
            </p>
        </div>
    """, unsafe_allow_html=True)

    user_email = st.text_input("Enter your partner ID or email to unlock Exponential Nodes", key="partner_email_input_exp")
    
    if st.button("Activate Exponential Tracking Node"):
        if user_email:
            ref_code = hashlib.md5(user_email.encode()).hexdigest()[:8]
            ref_link = f"https://growthengine-9btijzf8jcijy9hfqufsbu.streamlit.app/?ref={ref_code}&tier=exponential"
            
            st.success("Exponential tracking node locked successfully!")
            st.markdown(f"**Your Tier-1 Multiplier Link:** `{ref_link}`")
            
            st.markdown("""
                <div style="background: #1e1e1e; color: #4caf50; padding: 20px; border-radius: 12px; margin-top: 20px; border: 2px solid #4caf50;">
                    <div style="font-size: 16px; color: #fff; margin-bottom: 5px;">📊 Current Node Status: <span style="color: #4caf50;">Tier 1 Active (20% Yield)</span></div>
                    <div style="font-size: 14px; color: #ccc;">Bring just 2 referrals to auto-upgrade to Tier 2 (30% Yield / 1,500 USDT each). Bring 5 to unlock Tier 3 (40% Yield / 2,000 USDT each)!</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.warning("🔥 **Growth Command:** Share your link across all professional networks right now. Your multiplier increases automatically with every verified conversion!")
        else:
            st.warning("Please enter your partner ID or email first.")
