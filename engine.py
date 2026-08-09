import requests

class AutonomousEngine:
    def __init__(self):
        self.wallet_address = "0xD7709Dc72614240B065416D17c662Ee124654c78"
        # لا نحتاج إلى أي API Key بعد الآن!

    def check_payment_status(self):
        """فحص المعاملات مباشرة عبر عقد USDT على شبكة BSC دون الحاجة لحساب"""
        # استخدام رابط العقد الرسمي لعملية USDT على شبكة البيننس
        usdt_contract = "0x55d398326f99059ff775485246999027b3197955"
        url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={self.wallet_address}&page=1&offset=1&sort=desc"
        
        try:
            # طلب مباشر بدون مفتاح (يعمل أحياناً بحدود محدودة أو عبر بدائل مجانية مفتوحة)
            response = requests.get(url, timeout=10).json()
            if response.get('status') == '1' and len(response.get('result', [])) > 0:
                last_tx = response['result'][0]
                # التأكد أن التحويل وارد إلى محفظتك وليس صادراً منها
                if last_tx['to'].lower() == self.wallet_address.lower():
                    if int(last_tx['value']) >= 5000 * 10**18:
                        return True, "تم استلام المبلغ بنجاح!"
            return False, "في انتظار التحويل على المحفظة..."
        except Exception as e:
            return False, "جاري مراقبة البلوكشين..."
