import streamlit as st
from collector import fetch_site_data
from engine import analyze_performance

# 1. Page Configuration
st.set_page_config(page_title="GrowthEngine Audit", page_icon="⚡", layout="wide")

# 2. Extract Target URL from Query Parameters
query_params = st.query_params
default_url = query_params.get("target", "")

# 3. Main Header
st.title("⚡ GrowthEngine: Autonomous Web Audit & Instant Fix")
st.write("Perform live HTTP diagnostics, uncover actual performance bottlenecks, and deploy instant optimization patches.")

# 4. Input Field
target_url = st.text_input(
    "Enter your website or store URL:",
    value=default_url,
    placeholder="https://example.com",
    key="main_target_url_input"
)

# 5. Autonomous & Interactive Execution
auto_run = bool(default_url) and "evaluated" not in st.session_state

if st.button("Start Autonomous Audit", key="main_start_audit_btn") or auto_run:
    st.session_state["evaluated"] = True
    
    if target_url:
        with st.spinner("Analyzing live server latency and response headers..."):
            raw_data = fetch_site_data(target_url)
            results = analyze_performance(raw_data)
            
            st.success(f"Live audit completed successfully for: {target_url}")
            
            # تنظيف قيمة النتيجة لمنع تكرار علامة المئة %
            score_val = str(results.get("score", 0)).replace("%", "")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Live Server Latency", f"{raw_data.get('latency', 0)}s", "HTTP Response Time")
            col2.metric("Audit Health Score", f"{score_val}%", f"HTTP Status {raw_data.get('status_code', 200)}")
            col3.metric("Browser Caching", results.get("caching_status", "N/A"), "Cache-Control Directive")
            
            st.markdown("---")
            st.subheader("⚠️ Detected Bottlenecks & Code Vulnerabilities:")
            
            if results.get("issues"):
                for issue in results["issues"]:
                    st.warning(issue)
            else:
                st.success("Excellent! No critical server-side network issues detected.")
    else:
        st.error("Please enter a valid URL.")
