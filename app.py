import google.generativeai as genai

# إعداد مفتاح جوجل (يفضل سحبه من أسرار Streamlit Secrets)
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

with tab4:
    st.subheader("🤖 Autonomous AI Support & Objection Handler (Gemini Powered)")
    st.markdown("Directly powered by Google Gemini intelligence to handle any technical inquiry.")
    
    visitor_objection = st.text_input("Enter visitor question or doubt:")
    
    if st.button("Generate Intelligent Response"):
        if visitor_objection:
            with st.spinner("Analyzing inquiry with advanced Gemini intelligence..."):
                try:
                    # استخدام نموذج جيميني لتوليد الرد الفوري
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    prompt = f"You are a professional technical expert for GrowthEngine. Answer this visitor objection authoritatively and transparently about our blockchain acquisition system: {visitor_objection}"
                    
                    response = model.generate_content(prompt)
                    ai_reply = response.text
                    
                    st.success("AI Intelligence Response Generated:")
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; color: #31333F;">
                        {ai_reply}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"System Error: Could not connect to the intelligence layer. {e}")
        else:
            st.warning("Please enter a question.")
