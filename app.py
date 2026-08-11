import streamlit as st
import sqlite3
from collector import fetch_site_data
from engine import analyze_performance

st.set_page_config(page_title="GrowthEngine Autonomous Audit", page_icon="⚡", layout="wide")

# دالة الجلب من قاعدة البيانات التخزينية المباشرة
def get_cached_audit(domain_query):
    try:
        conn = sqlite3.connect("growth_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT latency, status_code, has_cache, score FROM audits WHERE domain LIKE ? OR audit_url LIKE ?", 
                       (f"%{domain_query}%", f"%{domain_query}%"))
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception:
        return None

# التخزين المؤقت للعمليات المباشرة لرفع كفاءة السيرفر عند الضغط العالي
@st.cache_data(ttl=1800, show_spinner=False)
def run_live_audit(url):
    raw = fetch_site_data(url)
    res = analyze_performance(raw)
    return raw, res

# 1. القراءة التلقائية للروابط المخصصة
query_params = st.query_params
default_url = query_params.get("target", "")

st.title("⚡ GrowthEngine: Autonomous Web Audit & Instant Fix")
st.write("Perform live HTTP diagnostics, uncover actual performance bottlenecks, and deploy instant optimization patches.")

target_url = st.text_input(
    "Enter your website or store URL:",
    value=default_url,
    placeholder="https://example.com",
    key="main_target_url_input"
)

auto_run = bool(default_url) and "evaluated" not in st.session_state

if st.button("Start Autonomous Audit", key="main_start_audit_btn") or auto_run:
    st.session_state["evaluated"] = True
    
    if target_url:
        cached_data = get_cached_audit(target_url)
        
        # استخدام البيانات الجاهزة إن وجدت لسرعة فائقة، أو إجراء فحص حي متزامن
        if cached_data:
            latency, status_code, has_cache, score = cached_data
            caching_status = "Enabled" if has_cache else "Missing Header"
            issues = []
            if latency > 1.0: issues.append(f"High Server Latency: {latency}s")
            if not has_cache: issues.append("Missing HTTP Cache-Control Header")
            
            st.success(f"Instant audit loaded for: {target_url}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Live Server Latency", f"{latency}s", "HTTP Response Time")
            col2.metric("Audit Health Score", f"{score}%", f"HTTP Status {status_code}")
            col3.metric("Browser Caching", caching_status, "Cache-Control Directive")
            
            st.markdown("---")
            st.subheader("⚠️ Detected Bottlenecks & Code Vulnerabilities:")
            if issues:
                for issue in issues:
                    st.warning(issue)
            else:
                st.success("Excellent! No critical server-side network issues detected.")
        else:
            with st.spinner("Analyzing live server latency and response headers..."):
                raw_data, results = run_live_audit(target_url)
                
                st.success(f"Live audit completed successfully for: {target_url}")
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
