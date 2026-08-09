with tab3:
    st.subheader("Performance-Based Referral Infrastructure (Limited 24H Window)")
    
    # رسالة تحذيرية تزيد من الإلحاح
    st.markdown("""
        <div style="background-color: #ffebee; border-left: 5px solid #f44336; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #d32f2f; margin-top: 0;">⚡ Flash 24-Hour Partner Window Active!</h3>
            <p style="color: #c62828; font-weight: bold;">
                Your eligibility to secure the <b>20% verified yield (1,000 USDT per referral)</b> expires strictly in 24 hours. 
                Share your link immediately to lock in your affiliate node access.
            </p>
        </div>
    """, unsafe_allow_html=True)

    user_email = st.text_input("Enter your partner ID or email to generate tracking link", key="partner_email_input")
    
    if st.button("Generate Secure Partner Link & Lock 24H Window"):
        if user_email:
            ref_code = hashlib.md5(user_email.encode()).hexdigest()[:8]
            ref_link = f"https://your-app-url.streamlit.app/?ref={ref_code}"
            
            st.success("Partner tracking link generated and locked successfully!")
            
            # عرض رابط الشريك
            st.markdown(f"**Your Unique Time-Sensitive Tracking Link:** `{ref_link}`")
            
            # العداد التنازلي الاحترافي (Live Countdown)
            st.markdown("""
                <div id="timer-box" style="text-align: center; background: #1e1e1e; color: #ff6154; padding: 20px; border-radius: 12px; margin-top: 20px; border: 2px solid #ff6154;">
                    <div style="font-size: 18px; color: #fff; margin-bottom: 10px;">⏳ Window Closes In:</div>
                    <div id="countdown" style="font-size: 32px; font-weight: bold; font-family: monospace;">24:00:00</div>
                </div>
                <script>
                    var totalSeconds = 24 * 60 * 60;
                    var display = document.getElementById('countdown');
                    var timer = setInterval(function() {
                        var h = Math.floor(totalSeconds / 3600);
                        var m = Math.floor((totalSeconds % 3600) / 60);
                        var s = totalSeconds % 60;
                        display.innerHTML = (h < 10 ? "0"+h : h) + ":" + (m < 10 ? "0"+m : m) + ":" + (s < 10 ? "0"+s : s);
                        if (totalSeconds <= 0) {
                            clearInterval(timer);
                            display.innerHTML = "EXPIRED";
                            document.getElementById('timer-box').style.borderColor = "#555";
                        }
                        totalSeconds--;
                    }, 1000);
                </script>
            """, unsafe_allow_html=True)
            
            st.info("🔥 **Strategy:** Post this link on your private professional groups, X, or LinkedIn immediately. Every referral converted through your node grants you 1,000 USDT automatically.")
        else:
            st.warning("Please enter a partner ID or email first.")
