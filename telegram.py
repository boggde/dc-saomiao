import time
import requests
from utils import format_money

from config import (
    TELEGRAM_ENABLED,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    RETRY_SEQUENCE,
    REQUEST_TIMEOUT
)



class Telegram:


    def __init__(self):

        self.enabled = TELEGRAM_ENABLED



    # ======================================
    # 发送消息
    # ======================================

    def send(
        self,
        text
    ):


        if not self.enabled:

            print(
                "[TELEGRAM DISABLED]"
            )

            return True



        if not TELEGRAM_BOT_TOKEN:

            print(
                "[TELEGRAM ERROR] Missing token"
            )

            return False



        url = (
            "https://api.telegram.org/bot"
            +
            TELEGRAM_BOT_TOKEN
            +
            "/sendMessage"
        )



        payload = {

            "chat_id":
                TELEGRAM_CHAT_ID,

            "text":
                text
        }



        for attempt in range(
            len(RETRY_SEQUENCE)+1
        ):


            try:

                response = requests.post(
                    url,
                    json=payload,
                    timeout=REQUEST_TIMEOUT
                )


                response.raise_for_status()



                print(
                    "[TELEGRAM OK]"
                )

                return True



            except Exception as e:


                print(
                    f"[TELEGRAM ERROR] {e}"
                )



                if attempt < len(RETRY_SEQUENCE):

                    delay = (
                        RETRY_SEQUENCE[attempt]
                    )

                    print(
                        f"[TELEGRAM RETRY] {delay}s"
                    )

                    time.sleep(
                        delay
                    )



        return False



    # ======================================
    # 启动测试通知
    # ======================================

    def startup_test(self):

        text = """
🚀 Binance Anomaly Monitor

状态:
✅ 程序启动成功
✅ Telegram连接正常
"""

        return self.send(
            text
        )



    # ======================================
    # 格式化报警
    # ======================================

    def format_alert(
        self,
        data
    ):


        return f"""
🚨 ==================
⭐:{data['symbol']}
1小时振幅:{data['range_pct']}%
当前价格:{data['price']}

High:{data['high']}Low:{data['low']}
1H Volume:{format_money(data['volume_1h'])} USDT
Volume Surge:{data['volume_multiple']}x
Time:{time.strftime('%Y-%m-%d %H:%M:%S')}
"""
