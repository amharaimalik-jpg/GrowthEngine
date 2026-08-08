import requests

class AutonomousEngine:
    def __init__(self):
        self.wallet_address = "0xD7709Dc72614240B065416D17c662Ee124654c78"
        self.bscscan_api_key = "YOUR_BSCSCAN_API_KEY" # سأشرح لك كيف تحصل عليه

    def check_payment_status(self):
        """مراقبة وصول المبلغ للعملات الرقمية على الشبكة"""
        url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress=0x55d398326f99059ff775485246999027b3197955&address={self.wallet_address}&apikey={self.bscscan_api_key}"
        try:
            response = requests.get(url).json()
            if response['status'] == '1':
                # فحص آخر معاملة تمت
                last_tx = response['result'][-1]
                # التحقق إذا كانت القيمة تعادل 5000 USDT (مع مراعاة الـ 18 خانة عشرية)
                if int(last_tx['value']) >= 5000 * 10**18:
                    return True, "تم استلام المبلغ بنجاح!"
            return False, "في انتظار التحويل..."
        except:
            return False, "خطأ في الاتصال بالشبكة."

    # بقية الدوال (generate_growth_report, etc) تبقى كما هي...
