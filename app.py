import streamlit as st
import requests
import hashlib

st.set_page_config(page_title="GrowthEngine: Sovereign Master Protocol", layout="wide", initial_sidebar_state="collapsed")

# --- SOVEREIGN PROTOCOL HEADER ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%); padding: 30px; border-radius: 16px; text-align: center; border: 2px solid #D4AF37; box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);">
    <h1 style="margin: 0; font-size: 32px; color: #D4AF37; font-family: monospace;">👑 GrowthEngine: Sovereign Master Protocol</h1>
    <p style="color: #ffffff; font-size: 16px; margin-top: 10px; font-weight: bold;">Public Access Closed. Exclusive Monopoly Allocation Active.</p>
    <div style="display: flex; justify-content: space-around; margin-top: 20px; background: #000; padding: 15px; border-radius: 8px;">
        <div>
            <span style="color: #888; font-size: 12px; display: block;">UPFRONT INFRASTRUCTURE TOLL</span>
            <span style="color: #00ff66; font-size: 20px; font-weight: bold;">$25,000 USD</span>
        </div>
        <div>
            <span style="color: #888; font-size: 12px; display: block;">EQUITY STAKE</span>
            <span style="color: #00ff66; font-size: 20px; font-weight: bold;">12.5% Co-founder Share</span>
        </div>
        <div>
            <span style="color: #888; font-size: 12px; display: block;">STATUS</span>
            <span style="color: #ff3333; font-size: 20px; font-weight: bold;">02 / 10 SEATS REMAINING</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PRE-LAUNCH / MONOPOLY ACCESS PASS BANNER ---
st.markdown("""
<div style="background: linear-gradient(135deg, #1b4d3e 0%, #0f2a22 100%); padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #00ff66;">
    <h2 style="margin: 0; color: #ffffff; font-size: 24px;">🔒 Pre-Launch Sovereign Allocation Pass</h2>
    <p style="color: #00ff66; font-size: 15px; margin-top: 5px; font-weight: bold;">Instant Infrastructure Wire ($25k) + 12.5% Equity Lock — Claim Your Sector Monopoly Now</p>
</div>
""", unsafe_allow_html=True)

# --- SECTOR MONOPOLY APPLICATION FORM ---
st.markdown("### **Secure Your Sovereign Sector Allocation**")
company_url = st.text_input("Enter your company domain or project URL (e.g., yourstartup.com)")
founder_email = st.text_input("Founder / CEO Secure Contact Email")

col1, col2 = st.columns(2)
with col1:
    industry_sector = st.selectbox("Select Target Industry Sector", ["Fintech & Payments", "SaaS & Enterprise AI", "Digital Assets & Web3", "Logistics & Marketplace"])
with col2:
    current_valuation = st.text_input("Current Company Valuation / Funding Stage", "Seed / Pre-Revenue / Growth")

if st.button("Transmit Sovereign Application ($25k + Equity Wire)"):
    if company_url and founder_email:
        st.success("Transmission received. Secure escrow channel and co-founder agreement dispatched to your secure communication line. Access restricted to verified wire originators.")
    else:
        st.error("Protocol Error: Complete all enterprise fields to initiate allocation review.")
