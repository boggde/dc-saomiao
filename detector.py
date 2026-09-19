import time

from config import (
    RANGE_THRESHOLD,
    ALERT_COOLDOWN_SECONDS
)



class Detector:


    def __init__(self):

        # 已成功发送报警的币
        # symbol -> timestamp

        self.cooldowns = {}



    # =========================================
    # 检查是否在冷却
    # =========================================

    def in_cooldown(
        self,
        symbol
    ):

        if symbol not in self.cooldowns:

            return False


        elapsed = (
            time.time()
            -
            self.cooldowns[symbol]
        )


        if elapsed >= ALERT_COOLDOWN_SECONDS:

            del self.cooldowns[symbol]

            return False


        return True



    # =========================================
    # 成功发送后进入冷却
    # =========================================

    def set_cooldown(
        self,
        symbol
    ):

        self.cooldowns[symbol] = time.time()



    # =========================================
    # 分析单个币
    # =========================================

    def analyze(
        self,
        symbol,
        history
    ):


        # 至少需要数据

        if len(history) < 2:

            return None



        prices = [
            x["price"]
            for x in history
        ]


        volumes = [
            x["volume"]
            for x in history
        ]



        high_price = max(
            prices
        )


        low_price = min(
            prices
        )

        current_price = prices[-1]

        # -------------------------------
        # 1小时方向判断
        # -------------------------------

        start_price = prices[0]

        # 当前价格 <= 1小时前价格
        # 说明不是上涨，过滤

        if current_price <= start_price:
            return None

        # -------------------------------
        # 1小时振幅
        # -------------------------------

        range_pct = (
                (high_price - low_price)
                /
                low_price
                *
                100
        )

        # -------------------------------
        # 1小时成交额
        # -------------------------------

        volume_1h = (
                volumes[-1]
                -
                volumes[0]
        )

        if volumes[0] > 0:

            normal_hour_volume = (
                    volumes[0]
                    /
                    24
            )

            volume_multiple = (
                    volume_1h
                    /
                    normal_hour_volume
            )

        else:

            volume_multiple = 0



        result = {

            "symbol":
                symbol,

            "price":
                current_price,

            "high":
                high_price,

            "low":
                low_price,

            "range_pct":
                round(
                    range_pct,
                    2
                ),

            "volume_1h":
                volume_1h,

            "volume_multiple":
                round(
                    volume_multiple,
                    2
                ),

            "timestamp":
                time.time()
        }



        # -------------------------------
        # 信号判断
        # -------------------------------

        if range_pct >= RANGE_THRESHOLD:

            result["signal"] = True

        else:

            result["signal"] = False



        return result