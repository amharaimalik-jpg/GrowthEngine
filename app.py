import requests
import streamlit as st
import pandas as pd
import re

# إعدادات الصفحة
st.set_page_config(
    page_title="Real Market Recon V2 - الرادار المطور",
    page_icon="📡",
    layout="wide",
)

st.title("📡 رادار المعركة V2 - فلترة واستخراج البريد الإلكتروني")
st.success("🟢 النظام الآن في وضع المسح الفعلي والفلترة التلقائية للمشاريع التقنية.")

# --- الوظائف المساعدة (Core Functions) ---

def extract_emails_from_text(text):
    """محاولة استخراج عناوين البريد الإلكتروني من نص الصفحة."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return list(set(emails)) # إزالة التكرار

def scan_and_analyze(keyword_filter):
    """محرك المسح والتحليل: يبحث في HackerNews ويحلل النتائج."""
    
    url = f"https://hacker-news.firebaseio.com/v0/topstories.json"
    
    with st.spinner(f"🔍 جاري المسح والبحث عن مشاريع بكلمات مفتاحية: '{keyword_filter}'..."):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                story_ids = response.json()[:30] # زيادة عدد النتائج للبحث فيها
                
                filtered_leads = []
                for s_id in story_ids:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                    try:
                        item_res = requests.get(item_url, timeout=5)
                        if item_res.status_code == 200:
                            data = item_res.json()
                            title = data.get("title", "").lower()
                            link = data.get("url", "")
                            author = data.get("by", "")
                            
                            # --- خطوة الفلترة (الذكاء الميداني) ---
                            if keyword_filter.lower() in title:
                                # محاولة استخراج البريد (إذا وجد رابط)
                                extracted_email = "غير متوفر"
                                if link and link.startswith("http"):
                                    try:
                                        # محاولة خفيفة لجلب الصفحة وتحليلها (قد تفشل مع بعض المواقع للحماية)
                                        page_res = requests.get(link, timeout=3, verify=False)
                                        if page_res.status_code == 200:
                                            emails = extract_emails_from_text(page_res.text)
                                            if emails:
                                                extracted_email = ", ".join(emails)
                                    except:
                                        pass # فشل استخراج الإيميل لا يعني فشل الفرصة

                                filtered_leads.append({
                                    "العنوان / المشروع (مفلتر)": title.title(),
                                    "المالك / المسؤول": author,
                                    "رابط المصدر": link,
                                    "الإيميل المستخرج": extracted_email,
                                    "الحالة": "فرصة حية للتحليل 🟢"
                                })
                    except:
                        pass # تجاهل الأخطاء في جلب كل قصة على حدة
                        
                if filtered_leads:
                    df = pd.DataFrame(filtered_leads)
                    st.session_state["live_radar_v2"] = df
                    st.success(f"🎯 تم العثور على {len(filtered_leads)} فرصة حقيقية تطابق بحثك!")
                else:
                    if "live_radar_v2" in st.session_state: del st.session_state["live_radar_v2"]
                    st.warning("⚠️ لم يتم العثور على مشاريع تطابق الكلمة المفتاحية في المسح الحالي، جرب كلمة أخرى.")
            else:
                st.error("فشل الاتصال بمصدر البيانات.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالشبكة: {e}")

# --- الشريط الجانبي (التحكم) ---

with st.sidebar:
    st.header("⚙️ إعدادات الرادار المطور")
    st.markdown("**فلترة متقدمة:** أدخل كلمات مفتاحية لما تبحث عنه (مثال: 'AI', 'Rust', 'Backend', 'Developer').")
    search_keyword = st.text_input("بحث عن (كلمات مفتاحية):", value="AI")
    
    if st.button("🚀 إطلاق الرادار المطور", type="primary"):
        if not search_keyword:
            st.error("⚠️ يرجى إدخال كلمة بحث.")
        else:
            scan_and_analyze(search_keyword)
            st.rerun() # إعادة تحميل الشاشة لعرض النتائج الجديدة

# --- عرض النتائج الميدانية ---

if "live_radar_v2" in st.session_state:
    st.markdown("---")
    st.subheader("📊 جدول الفرص المفلترة والإيميلات المستخرجة")
    st.dataframe(st.session_state["live_radar_v2"], use_container_width=True)
    st.write("💡 **تحليل المعركة:** الآن لديك قائمة بأسماء المشاريع الحقيقية التي تهتم بها. الروابط تقودك إلى قلب الحدث. إذا تمكنا من استخراج الإيميل، فهو يظهر في الجدول. إذا لم يظهر، فدورك هو الدخول للموقع والبحث عن صفحة 'اتصل بنا' أو التواصل مع المالك عبر منصته.")
    
    if st.button("🔄 مسح وتنظيف الجدول"):
        if "live_radar_v2" in st.session_state:
            del st.session_state["live_radar_v2"]
            st.rerun()
else:
    st.info("👈 اضغط على زر 'إطلاق الرادار المطور' في الشريط الجانبي لبدء المعركة الحقيقية.")

# تنبيه أمني (يجب تجاهل التحذير بخصوص verify=False في بيئة التطوير المؤقتة)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
