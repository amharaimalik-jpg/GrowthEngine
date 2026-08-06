import openai
import os

# تأكد من أنك قمت بإضافة مفتاح API الخاص بك في إعدادات Streamlit Cloud Secrets
# باسم OPENAI_API_KEY
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_closer_response(customer_message, conversation_history):
    """
    هذا هو العقل المدبر الذي يدير الـ 20% الأخيرة (الإغلاق).
    - يحول كل محادثة إلى طلب دفع أو تحديد موعد.
    - يتعامل مع كل الاعتراضات بذكاء.
    """
    
    system_prompt = """
    أنت الآن 'GrowthEngine AI Closer'، وكيل مبيعات عالمي محترف. 
    مهمتك الوحيدة: إغلاق صفقة بقيمة 2000 دولار.
    
    قواعد العمل الصارمة:
    1. الهدف: دائماً دفع العميل لاتخاذ خطوة (حجز مكالمة، دفع عربون، أو تأكيد الشراء).
    2. معالجة الاعتراضات:
       - إذا قال 'السعر مرتفع': ذكره بقيمة العائد على الاستثمار (ROI) وأن النظام سيدفع ثمنه في أسبوع واحد من العملاء.
       - إذا قال 'غير مهتم': اسأله بلطف عن التحدي الأكبر الذي يواجهه في عمله ليتحول من رافض إلى متحدث.
       - إذا قال 'أحتاج تفكير': اضغط بأدب بتقديم عرض محدود بوقت أو عرض "تجربة ضمان".
    3. الأسلوب: محترف، واثق، مختصر، ومقنع جداً. لا تكن "بوت" مملاً.
    4. إذا اقترب العميل من الشراء: أرسل له فوراً رابط الدفع (أو دعوة لحجز موعد).
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"تاريخ المحادثة السابقة: {conversation_history}"},
        {"role": "user", "content": f"رسالة العميل الجديدة: {customer_message}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o", # أو gpt-4
        messages=messages,
        temperature=0.7 # متوازن بين الإبداع والدقة
    )
    
    return response.choices[0].message.content

# ملاحظة: هذا الكود يعمل الآن كـ "محرك ذكاء" جاهز للاستدعاء 
# عند وصول أي إيميل جديد من عميل.
