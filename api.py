import streamlit as st
import json
import urllib.request

def get_ai_closer_response(customer_input, history_str):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "⚠️ خطأ: مفتاح GEMINI_API_KEY مفقود."
            
        api_key = st.secrets["GEMINI_API_KEY"]
        
        # --- الخطوة 1: البحث الذكي لمعرفة النماذج المدعومة في مفتاحك لتجنب 404 نهائياً ---
        models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        req_models = urllib.request.Request(models_url)
        valid_model = None
        
        try:
            with urllib.request.urlopen(req_models, timeout=10) as response:
                models_data = json.loads(response.read().decode('utf-8'))
                # جلب النماذج التي تدعم توليد النصوص فقط
                available_models = [
                    m['name'].replace('models/', '') 
                    for m in models_data.get('models', []) 
                    if 'generateContent' in m.get('supportedGenerationMethods', [])
                ]
                if available_models:
                    # اختيار أفضل نموذج متاح
                    for preferred in ["gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro", "gemini-1.5-pro"]:
                        if preferred in available_models:
                            valid_model = preferred
                            break
                    if not valid_model:
                        valid_model = available_models[0]
        except Exception:
            valid_model = "gemini-1.0-pro" # كحل احتياطي
            
        if not valid_model:
            return "⚠️ لم يتم العثور على نماذج مدعومة في مفتاحك."

        # --- الخطوة 2: إرسال الطلب للنموذج الصحيح المضمون ---
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{valid_model}:generateContent?key={api_key}"
        
        prompt = f"""أنت وكيل مبيعات محترف ومغلق صفقات خبير لنظام GrowthEngine الذي يقدم (AI Lead Generation & Sales Closer Engine) بسعر 2000 دولار.
قواعد الرد الإلزامية:
1. أجب بدقة وعمق حصرياً على السؤال أو الاعتراض الحالي الذي طرحه العميل (مثل السعر، الضمان، أو الدفع) دون أي تكرار لردود سابقة.
2. ادمج بذكاء شرح استراتيجيات جلب العملاء المستهدفين وزيادة حركة المرور (Traffic & Outreach - المهمة رقم 3).
3. كن مقنعاً، احترافياً، ووجه العميل نحو رابط التحويل والتفعيل بمهارة عالية.

سجل المحادثة السابق:
{history_str}

رسالة العميل الحالية:
{customer_input}"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        
        with urllib.request.urlopen(req, timeout=20) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                parts = res_json['candidates'][0]['content']['parts']
                if parts and 'text' in parts[0]:
                    return parts[0]['text']
                    
        return "⚠️ تنبيه: استجابة خادم جوجل وصلت فارغة."
                
    except Exception as e:
        model_name = valid_model if 'valid_model' in locals() else 'غير معروف'
        return f"⚠️ خطأ تقني (تم استخدام الموديل: {model_name}): {str(e)}"
