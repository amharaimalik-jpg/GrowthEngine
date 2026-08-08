import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Engineering Opportunity Miner - صائد الفرص",
    page_icon="🛠️",
    layout="wide",
)

st.title("🛠️ صائد الفرص الهندسية والحقيقية")
st.success("🟢 النظام متصل ومبرمج لتحليل المشاريع الحية وتوليد مقترحات هندسية جاهزة للتقديم.")

with st.sidebar:
    st.header("⚙️ إعدادات الصائد")
    tech_focus = st.selectbox("اختر التخصص التقني للهندسة:", ["AI & Machine Learning", "Backend & Python", "Systems & Rust"])
    keyword = st.text_input("كلمة البحث المخصصة:", value="AI")
    
    if st.button("🚀 ابدأ صيد وتحليل الفرص", type="primary"):
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                story_ids = res.json()[:25]
                mined_leads = []
                
                for s_id in story_ids:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                    item_res = requests.get(item_url, timeout=5)
                    if item_res.status_code == 200:
                        data = item_res.json()
                        title = data.get("title", "")
                        link = data.get("url", "https://news.ycombinator.com")
                        author = data.get("by", "مطور مستقل")
                        
                        if keyword.lower() in title.lower():
                            proposal = f"مرحباً، لاحظت مشروعكم ({title}). بصفتي مهندس برمجيات، يمكنني مساعدتكم في تحسين كفاءة البنية التحتية، تسريع الأداء، وتخفيض تكاليف التشغيل بنسبة تصل إلى 40% عبر هندسة الأنظمة المتقدمة."
                            
                            mined_leads.append({
                                "اسم المشروع / الفرصة": title,
                                "المالك / المسؤول": author,
                                "رابط المشروع الحقيقي": link,
                                "التقرير الهندسي المقترح للتقديم": proposal,
                                "حالة الفرصة": "جاهزة للتواصل الفعلي 🟢"
                            })
                
                if mined_leads:
                    st.session_state["mined_data"] = pd.DataFrame(mined_leads)
                    st.success(f"🎯 تم صيد وتحليل {len(mined_leads)} فرصة هندسية بنجاح!")
                else:
                    st.warning("⚠️ لم يتم العثور على نتائج مطابقة، جرب كلمة بحث أخرى.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")

if "mined_data" in st.session_state:
    st.markdown("---")
    st.subheader("📊 لوحة الفرص الهندسية والرسائل الجاهزة للتواصل")
    st.dataframe(st.session_state["mined_data"], use_container_width=True)
    
    st.markdown("### 💡 الخطوة الفاصلة لتحقيق الأرباح الحقيقية:")
    st.write("1. اضغط على رابط المشروع الحقيقي من الجدول بالأعلى وتوجه لصفحته أو حسابه.")
    st.write("2. انسخ **'التقرير الهندسي المقترح'** المخصص لهذا المشروع.")
    st.write("3. أرسل العرض للمالك عبر البريد أو منصته. عندما يرى أنك تقدم حلاً حقيقياً لمشروعه التقني، هنا يبدأ التعاقد الفعلي وتحويل الأرباح لحسابك بناءً على مهاراتك الهندسية الخالصة.")
    
    if st.button("🔄 إعادة ضبط الصائد"):
        del st.session_state["mined_data"]
        st.rerun()
else:
    st.info("👈 اضغط على زر 'ابدأ صيد وتحليل الفرص' في الشريط الجانبي لبدء المعركة الحقيقية واستخراج الفرص الآن.")
