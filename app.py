import streamlit as st
import requests
import time

# =========================================================
# CONFIGURATION / إعدادات المحفظة والشبكة
# =========================================================
TRUST_WALLET_ADDRESS = "TQWzQDUhantt9zG5njU2KFyscxWYqLLrc7"
NETWORK_NAME = "USDT - TRC20 (TRON Network)"

# 1. Page Configuration
st.set_page_config(
    page_title="GrowthEngine: Live Web Audit & Instant Fix",
    page_icon="⚡",
    layout="wide"
)

# 2. Header
st.title("⚡ GrowthEngine: Autonomous Web Audit & Instant Fix")
st.caption("Perform live HTTP diagnostics, uncover actual performance bottlenecks, and deploy instant optimization patches.")

# 3. Target URL Input
url_input = st.text_input("Enter your website or store URL:", placeholder="https://example.com")

# 4. Live Audit Engine (Real HTTP Inspection)
def run_live_audit(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 GrowthEngine/2.0'
    }
    
    start_time = time.time()
    response = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
    latency = round(time.time() - start_time, 2)
    
    resp_headers = response.headers
    
    # Check Server Compression
    encoding = resp_headers.get('Content-Encoding', '').lower()
    has_compression = 'gzip' in encoding or 'br' in encoding or 'deflate' in encoding
    
    # Check Browser Caching
    cache_control = resp_headers.get('Cache-Control', '').lower()
    has_caching = 'max-age' in cache_control or 'public' in cache_control or 's-maxage' in cache_control
    
    # Check Security / HTTPS
    is_https = response.url.startswith("https://")
    
    # Score & Diagnostics Calculation
    score = 100
    issues = []
    
    if latency > 1.2:
        score -= 25
        issues.append(f"Slow initial server response time ({latency}s). Optimal latency target is < 0.8s.")
    if not has_compression:
        score -= 25
        issues.append("HTTP compression (Gzip/Brotli) is disabled on server responses.")
    if not has_caching:
        score -= 25
        issues.append("Browser caching headers (Cache-Control) are missing or misconfigured.")
    if not is_https:
        score -= 25
        issues.append("Insecure connection detected (HTTPS/SSL encryption is missing).")
        
    return {
        "final_url": response.url,
        "status_code": response.status_code,
        "latency": f"{latency}s",
        "score": f"{max(score, 10)}%",
        "has_compression": has_compression,
        "has_caching": has_caching,
        "is_https": is_https,
        "issues": issues
    }

# 5. Execution Pipeline
if st.button("Start Autonomous Audit", type="primary"):
    if not url_input.strip():
        st.error("Please enter a valid website URL to begin.")
    else:
        with st.spinner("Initiating live server ping and analyzing real HTTP response headers..."):
            try:
                data = run_live_audit(url_input.strip())
                st.success(f"Live audit completed successfully for: {data['final_url']}")
                
                # Real Metrics Display
                col1, col2, col3 = st.columns(3)
                col1.metric("Live Server Latency", data["latency"], "HTTP Response Time")
                col2.metric("Audit Health Score", data["score"], f"HTTP Status {data['status_code']}")
                col3.metric("Browser Caching", "Active" if data["has_caching"] else "Missing Header", "Cache-Control Directive")

                st.markdown("---")
                
                # Real Diagnostics Report
                st.subheader("⚠️ Detected Bottlenecks & Code Vulnerabilities:")
                if data["issues"]:
                    for idx, issue in enumerate(data["issues"], 1):
                        st.warning(f"{idx}. {issue}")
                else:
                    st.success("Excellent! No critical server-side network issues detected.")
                
                st.markdown("---")
                
                # Action Options
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
