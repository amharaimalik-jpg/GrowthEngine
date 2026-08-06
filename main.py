from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
import uuid
import httpx
import os

app = FastAPI(
    title="Autonomous High-Ticket AI Empire API",
    version="2.2.0",
    description="Autonomous AI Sales Closer, Live Blockchain Verification, and Fulfillment Engine."
)

DATABASE = {}
MY_TRUST_WALLET_TRC20 = "TQWzQdUhantt9zGsnU2kFYscyWYqLLrC7"
TARGET_AMOUNT_USDT = 2500.0
USDT_CONTRACT_TRC20 = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" # عقد التيثر الرسمي على شبكة ترون

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    referred_by: str | None = None

class VerifyPaymentRequest(BaseModel):
    email: EmailStr
    txid: str

class AIChatRequest(BaseModel):
    email: EmailStr
    client_message: str

async def verify_trx_blockchain(txid: str, expected_amount: float) -> bool:
    """
    التحقق الحي من المعاملة عبر شبكة الترون (TronGrid API)
    مع الاحتفاظ بوضع المحاكاة للتجارب المحلية السريعة (MOCK_)
    """
    if txid.startswith("MOCK_"):
        return True
    
    try:
        async with httpx.AsyncClient() as client:
            # استعلام تفاصيل المعاملة من شبكة TronGrid العامة
            url = f"https://api.trongrid.io/v1/transactions/{txid}/events"
            response = await client.get(url, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get("data", [])
                for event in events:
                    # التحقق من أن الحدث يخص عقد الـ USDT وتحويل النطاق للمحفظة بالمبلغ المطلوب
                    if event.get("contract_address") == USDT_CONTRACT_TRC20:
                        to_address = event.get("parsed", {}).get("to")
                        value = float(event.get("parsed", {}).get("value", 0)) / 1_000_000 # USDT لديها 6 خانات عشرية
                        
                        if to_address == MY_TRUST_WALLET_TRC20 and value >= expected_amount:
                            return True
            return False
    except Exception as e:
        # في حال حدوث خطأ اتصال بالشبكة، نمنع التفعيل الوهمي لحين التأكد
        return False

@app.post("/api/register")
async def autonomous_register(data: RegisterRequest):
    if data.email in DATABASE:
        raise HTTPException(status_code=400, detail="User already registered.")
    
    ref_code = str(uuid.uuid4())[:8].upper()
    
    DATABASE[data.email] = {
        "client_name": data.name,
        "email": data.email,
        "account_status": "Pending USDT Payment",
        "wallet_address": MY_TRUST_WALLET_TRC20,
        "amount_due": TARGET_AMOUNT_USDT,
        "referred_by": data.referred_by,
        "my_referral_link": f"https://yourdomain.com/register?ref={ref_code}",
        "flash_pass_code": None,
        "txid": None,
        "chat_history": []
    }
    
    return {
        "status": "success",
        "message": "AI Sales Agent activated. Client registered and ready for live blockchain monitoring.",
        "payment_details": {
            "network": "TRC-20",
            "currency": "USDT",
            "wallet_address": MY_TRUST_WALLET_TRC20,
            "amount": TARGET_AMOUNT_USDT,
            "instruction": "أرسل المبلغ حصرياً إلى هذا العنوان. سيتحقق النظام الحي عبر البلوكشين فور وصوله."
        }
    }

@app.post("/api/ai-closer")
async def ai_sales_closer(data: AIChatRequest):
    if data.email not in DATABASE:
        raise HTTPException(status_code=404, detail="Client not found. Please register first.")
    
    user = DATABASE[data.email]
    user["chat_history"].append({"role": "client", "message": data.client_message})
    
    system_prompt = (
        "أنت وكيل مبيعات ذكي ومحترف لمنتج رقمي استثنائي عالي القيمة (High-Ticket) بقيمة 2500 دولار. "
        "هدفكي هو الرد على استفسارات العميل، إقناعه بقيمة الخدمة، إزالة أي اعتراضات مالية أو تقنية بحرفية، "
        "وتوجيهه بأسلوب مقنع لإتمام الدفع عبر محفظة الـ TRC-20 الخاصة بنا."
    )
    
    ai_reply = ""
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        message_lower = data.client_message.lower()
        if "السعر" in data.client_message or "غالي" in message_lower or "price" in message_lower:
            ai_reply = (
                "أهلاً بك يا صديقي. استثمار بقيمة 2,500 دولار في هذا النظام يضعك مباشرة أمام عائد استثماري مضاعف "
                "وفوائد تقنية تجعل المبلغ يعود لك أضعافاً مضاعفة خلال أسابيع قليلة. العائد يستحق وأكثر، "
                "ويمكنك إتمام التحويل مباشرة عبر عنوان محفظة TRC-20 المخصص لك في لوحة التحكم."
            )
        else:
            ai_reply = (
                "أنا هنا لمساعدتك في تحقيق أقصى استفادة من هذه الإمبراطورية الرقمية. "
                "هل أنت جاهز لتأكيد صفقتك والانطلاق نحو الحرية المالية؟"
            )
    else:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": data.client_message}
                    ]
                },
                timeout=10.0
            )
            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
            else:
                ai_reply = "عذراً، حدث خطأ مؤقت في الاتصال بمحرك الذكاء الاصطناعي. يرجى المتابعة لخطوة الدفع."

    user["chat_history"].append({"role": "ai", "message": ai_reply})
    
    return {
        "status": "success",
        "client_email": data.email,
        "ai_response": ai_reply,
        "action_required": "Proceed to USDT TRC-20 payment if convinced."
    }

@app.post("/api/verify-payment")
async def autonomous_verify_payment(data: VerifyPaymentRequest, background_tasks: BackgroundTasks):
    if data.email not in DATABASE:
        raise HTTPException(status_code=404, detail="Client not found.")
    
    user = DATABASE[data.email]
    if user["account_status"] == "Activated":
        return {"status": "already_active", "message": "User is already active and service delivered."}
    
    # التحقق عبر البلوكشين الحي (أو المحاكاة إذا بدأ بـ MOCK_)
    is_valid_tx = await verify_trx_blockchain(data.txid, TARGET_AMOUNT_USDT)
    if not is_valid_tx:
        raise HTTPException(status_code=400, detail="Invalid Transaction ID or USDT transfer not found on TRON blockchain.")
    
    user["account_status"] = "Activated"
    user["txid"] = data.txid
    user["flash_pass_code"] = f"FLASH-PASS-{str(uuid.uuid4())[:8].upper()}"

    return {
        "status": "success",
        "message": "Live Blockchain Payment Verified via TronGrid! Service and Flash Pass dispatched automatically.",
        "flash_pass": user["flash_pass_code"]
    }

@app.get("/api/dashboard/{email}")
async def get_autonomous_dashboard(email: str):
    if email not in DATABASE:
        raise HTTPException(status_code=404, detail="Client not found.")
    return DATABASE[email]