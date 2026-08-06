# app.py
import streamlit as st
import db_manager
import offer_config
import scraper
import outreach
import payment_gateway
import pandas as pd

st.set_page_config(page_title="GrowthEngine Web Dashboard", page_icon="🚀", layout="wide")

st.title("🚀 GrowthEngine Master Control Center - Web Dashboard")
st.markdown(f"### 💡 Active Offer: `{offer_config.OFFER_TITLE}` | Price: **${offer_config.OFFER_PRICE} USD**")

# القائمة الجانبية للتحكم
st.sidebar.header("🎛️ Navigation Panel")
choice = st.sidebar.radio("Select Operation", [
    "📊 Database & Leads", 
    "⚡ Run Full Pipeline", 
    "💰 Financial Analytics"
])

if choice == "📊 Database & Leads":
    st.subheader("📋 Live SQLite Database Records")
    rows = db_manager.get_all_leads()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Niche", "Status"])
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("[-] Database is empty. Run the pipeline from the sidebar first.")

elif choice == "⚡ Run Full Pipeline":
    st.subheader("⚙️ Automated Empire Pipeline Execution")
    if st.button("🚀 Launch Full Pipeline Now"):
        with st.spinner("Executing pipeline (Scraping -> Outreach -> Collection)..."):
            scraper.generate_target_leads()
            outreach.launch_outbound_campaign()
            payment_gateway.process_incoming_payments()
        st.success("🌟 Full Pipeline Completed Successfully! Database and Revenue Updated!")

elif choice == "💰 Financial Analytics":
    st.subheader("💎 Executive Financial & Performance Metrics")
    rows = db_manager.get_all_leads()
    if rows:
        total_clients = len(rows)
        paid_clients = sum(1 for r in rows if r[4] == 'Paid')
        revenue = paid_clients * 2000
        pipeline = total_clients * 2000
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Target Leads", total_clients)
        col2.metric("Secured Paid Clients", paid_clients)
        col3.metric("Total Revenue Generated", f"${revenue:,} USD")
        
        st.markdown("---")
        st.bar_chart(pd.DataFrame({"Revenue": [revenue]}, index=["GrowthEngine V1"]))
    else:
        st.warning("[-] No data found to calculate analytics.")