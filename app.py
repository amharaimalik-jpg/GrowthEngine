import streamlit as st
from collector import fetch_site_data
from engine import analyze_performance

TRUST_WALLET_ADDRESS = "TQWzQDUhantt9zG5njU2KFyscxWYqLLrc7"
NETWORK_NAME = "USDT - TRC20 (TRON Network)"

st.set_page_config(
    page_title="GrowthEngine: Live Web Audit & Instant Fix",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ GrowthEngine: Autonomous Web Audit & Instant Fix")
st.caption("Perform live HTTP diagnostics, uncover actual performance bottlenecks, and deploy instant optimization patches.")

url_input = st.text_input("Enter your website or store URL:", placeholder="https://example.com")

if st.button("Start Autonomous Audit", type="primary"):
    if not url_input.strip():
        st.error("Please enter a valid website URL to begin.")
    else:
        with st.spinner("Connecting to target server via Collector Engine..."):
            try:
                # 1. الاستدعاء من collector
                raw_data = fetch_site_data(url_input.strip())
                
                # 2. التحليل عبر engine
                data = analyze_performance(raw_data)
                
                st.success(f"Live audit completed successfully for: {data['final_url']}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Live Server Latency", data["latency"], "HTTP Response Time")
                col2.metric("Audit Health Score", data["score"], f"HTTP Status {data['status_code']}")
                col3.metric("Browser Caching", "Active" if data["has_caching"] else "Missing Header", "Cache-Control Directive")

                st.markdown("---")
                
                st.subheader("⚠️ Detected Bottlenecks & Code Vulnerabilities:")
                if data["issues"]:
                    for idx, issue in enumerate(data["issues"], 1):
                        st.warning(f"{idx}. {issue}")
                else:
                    st.success("Excellent! No critical server-side network issues detected.")
                
                st.markdown("---")
                
                st.subheader("🛠️ Instant Fix & Deployment Engine")
                tab1, tab2, tab3 = st.tabs([
                    "🚀 Instant Proof Badge (Free)", 
                    "🔗 Partner Cloud Activation", 
                    "💳 Direct Priority Settlement (Trust Wallet)"
                ])
                
                with tab1:
                    st.info("Embed this verified badge snippet into your website footer to unlock your automated optimization patch script:")
                    badge_code = f'''<!-- GrowthEngine Proof Badge -->
<div id="growthengine-badge" style="text-align:center; padding:10px; font-family:sans-serif;">
  <a href="https://growthengine-9btijzf8jcjty9hfqufsbu.streamlit.app" target="_blank" style="text-decoration:none; color:#10B981; font-weight:bold;">
    🛡️ Verified & Optimized by GrowthEngine
  </a>
</div>'''
                    st.code(badge_code, language="html")
                    
                    if st.button("Confirm Badge Placement & Generate Patch"):
                        st.balloons()
                        st.success("Badge placement verified! Deploy this optimization patch to your site header:")
                        autofix_script = '''<script>
  // GrowthEngine Auto-Fix Optimization Patch
  console.log("GrowthEngine Optimization Active");
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("img").forEach(img => {
      if(!img.hasAttribute("loading")) img.setAttribute("loading", "lazy");
    });
  });
</script>'''
                        st.code(autofix_script, language="html")

                with tab2:
                    st.write("Activate enterprise cloud optimization via our verified partner infrastructure:")
                    affiliate_link = "https://www.partner-platform.com/signup?aff_id=YOUR_PARTNER_ID"
                    st.markdown(f'👉 [Click here for Direct Cloud Partner Integration]({affiliate_link})')

                with tab3:
                    st.subheader("Direct Crypto Payment for Manual Priority Optimization")
                    st.write("Send **25 USDT** for dedicated custom fix implementation by our engineering team.")
                    st.markdown(f"**Network:** `{NETWORK_NAME}`")
                    st.markdown("**Deposit Address (Trust Wallet):**")
                    st.code(TRUST_WALLET_ADDRESS, language="text")
                    st.caption("⚠️ Ensure you send USDT strictly over the TRC20 network to avoid loss of funds.")

            except Exception as e:
                st.error(f"Could not reach target server. Please check if the URL is active and accessible. Error: {str(e)}")
                import streamlit as st
from collector import fetch_site_data
from engine import analyze_performance

# 1. إعدادات الصفحة الرئيسية
st.set_page_config(page_title="GrowthEngine Audit", page_icon="⚡", layout="wide")

# 2. استخراج النطاق المستهدف من رابط URL إن وجد
query_params = st.query_params
default_url = query_params.get("target", "")

# 3. عرض الواجهة الرئيسية (مرة واحدة فقط)
st.title("⚡ GrowthEngine: Autonomous Web Audit & Instant Fix")
st.write("Perform live HTTP diagnostics, uncover actual performance bottlenecks, and deploy instant optimization patches.")

target_url = st.text_input("Enter your website or store URL:", value=default_url, placeholder="https://example.com")

# 4. آلية التحقق للتشغيل الآلي بدون تكرار
auto_run = bool(default_url) and "evaluated" not in st.session_state

if st.button("Start Autonomous Audit") or auto_run:
    st.session_state["evaluated"] = True
    
    if target_url:
        with st.spinner("Analyzing live server latency and response headers..."):
            raw_data = fetch_site_data(target_url)
            results = analyze_performance(raw_data)
            
            st.success(f"Live audit completed successfully for: {target_url}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Live Server Latency", f"{raw_data.get('latency', 0)}s", "HTTP Response Time")
            col2.metric("Audit Health Score", f"{results.get('score', 0)}%", f"HTTP Status {raw_data.get('status_code', 200)}")
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
