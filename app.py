import requests
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(
    page_title="Battle Station - غرفة عمليات الأرباح",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ غرفة عمليات الأرباح - التنفيذ الميداني الشامل")
st.success("🟢 النظام في وضع الهجوم الفوري: صيد الفرصة + تجهيز العرض + الإرسال المباشر.")

with st.sidebar:
    st.header("⚙️ مركز الإطلاق")
    keyword = st.text_input("مجال الاستهداف التقني:", value="AI")
    
    if st.button("🚀 اطلق عملية اقتناص الأرباح", type="primary"):
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                story_ids = res.json()[:20]
                action_leads = []
                
                for s_id in story_ids:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                    item_res = requests.get(item_url, timeout=5)
                    if item_res.status_code == 200:
                        data = item_res.json()
                        title = data.get("title", "")
                        link = data.get("url", "https://news.ycombinator.com")
                        author = data.get("by", "مطور مستقل")
                        
                        if keyword.lower() in title.lower():
                            # صياغة التقرير الهندسي الاحترافي للعميل
                            proposal_text = f"مرحباً {author}، لاحظت مشروعكم ({title}). بصفتي مهندس برمجيات، يمكنني تطوير البنية التحتية، تسريع الأداء، وخفض تكاليف التشغيل بنسبة 40% عبر هندسة الأنظمة المتقدمة. هل تود مناقشة تفاصيل التعاون؟"
                            
                            # تجهيز رابط الإرسال المباشر
                            encoded_body = urllib.parse.quote(proposal_text)
                            encoded_subject = urllib.parse.quote(f"عرض هندسي لتحسين مشروعك: {title}")
                            mailto_link = f"mailto:?subject={encoded_subject}&body={encoded_body}"
                            
                            action_leads.append({
                                "المشروع": title,
                                "المالك": author,
                                "رابط المصدر": link,
                                "التقرير الهندسي": proposal_text,
                                "رابط الإرسال الفوري": mailto_link
                            })
                
                if action_leads:
                    st.session_state["action_data"] = pd.DataFrame(action_leads)
                    st.success(f"🎯 تم رصد وتجهيز {len(action_leads)} هدف حقيقي بنجاح!")
                else:
                    st.warning("⚠️ لم يتم العثور على نتائج مطابقة، جرب كلمة بحث أخرى.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")

if "action_data" in st.session_state:
    st.markdown("---")
    st.subheader("🎯 أهداف المعركة الجاهزة للتنفيذ الفوري والتواصل")
    
    df = st.session_state["action_data"]
    for idx, row in df.iterrows():
        with st.container():
            st.markdown(f"### 🔹 الهدف #{idx+1}: {row['المشروع']}")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**المالك / المسؤول:** {row['المالك']} | [🔗 رابط المشروع الحقيقي]({row['رابط المصدر']})")
                st.info(f"**التقرير الهندسي الجاهز:**\n\n{row['التقرير الهندسي']}")
            with col2:
                st.markdown("---")
                st.markdown(f"[✉️ إرسال العرض فوراً عبر البريد]({row['رابط الإرسال الفوري']})")
                st.write("*(أو انسخ النص وتوجه لصفحة المشروع مباشرة)*")
            st.markdown("---")
    
    if st.button("🔄 إعادة ضبط غرفة العمليات"):
        del st.session_state["action_data"]
        st.rerun()
else:
    st.info("👈 اضغط على زر 'اطلق عملية اقتناص الأرباح' في الشريط الجانبي لبدء المعركة الميدانية الكاملة الآن.") 
