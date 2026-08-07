import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = "أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار. هدفك الرد باحترافية وإقناع العميل وإغلاق الصفقة."
        
        prompt = f"{system_instruction}\n\nسجل المحادثة السابق:\n{history_str}\n\nرسالة العميل الحالية: {customer_input}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
                # تنسيق الرد القادم من الذكاء الاصطناعي بدعم الاتجاه الصحيح
                return f'<div dir="rtl" style="text-align: right;">{raw_text}</div>'
    except Exception:
        pass
        
    # تنسيق HTML مباشر يمنع أي انعكاس أو تداخل في النصوص والأرقام
    return """<div dir="rtl" style="text-align: right; line-height: 1.6;">
أهلاً بك يا صديقي، أتفهم تماماً حرصك على رأس مالك، وهذا ما يميّز رائد الأعمال الذكي.<br><br>
نظام <b>GrowthEngine</b> مصمم خصيصاً ليحقق لك العائد الاستثماري السريع خلال أول 14 يوماً. إليك خطة العمل المباشرة لنبدأ اليوم:<br><br>
• <b>أول 48 ساعة:</b> إطلاق محرك استقطاب العملاء لجلب أول 50 عميل مستهدف بدقة عالية لعملك.<br>
• <b>من يوم 3 إلى 7:</b> تفعيل وكيل الإغلاق الذكي للرد الفوري وتصفية المهتمين وإغلاق الصفقات على مدار الساعة.<br>
• <b>ضمان استرداد رأس المال:</b> النظام مصمم ليغلق صفقات تعوض مبلغ الـ 2000 دولار بالكامل خلال أول 3 أسابيع كحد أقصى.<br><br>
<b>رابط التحويل وتفعيل النظام جاهز الآن.. لنبدأ رحلة مضاعفة أرباحك اليوم! 🚀</b>
</div>"""
