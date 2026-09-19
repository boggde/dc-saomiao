from collections import defaultdict, deque
import time

from config import HISTORY_SECONDS


class Storage:

    def __init__(self):

        # 每个币保存最近1小时数据
        #
        # symbol:
        # [
        #   {
        #       time,
        #       price,
        #       volume
        #   }
        # ]

        self.history = defaultdict(
            lambda: deque(maxlen=500)
        )


    # =====================================
    # 添加数据
    # =====================================

    def add(
        self,
        symbol,
        price,
        volume
    ):

        now = time.time()


        self.history[symbol].append(
            {
                "time": now,
                "price": float(price),
                "volume": float(volume)
            }
        )


        self.cleanup(
            symbol,
            now
        )



    # =====================================
    # 删除超过1小时数据
    # =====================================

    def cleanup(
        self,
        symbol,
        now
    ):

        queue = self.history[symbol]


        while queue:


            if (
                now - queue[0]["time"]
                >
                HISTORY_SECONDS
            ):

                queue.popleft()


            else:

                break



    # =====================================
    # 获取历史
    # =====================================

    def get(
        self,
        symbol
    ):

        return list(
            self.history.get(
                symbol,
                []
            )
        )



    # =====================================
    # 当前状态
    # =====================================

    def status(self):

        ready = 0

        total = len(
            self.history
        )


        now = time.time()


        for symbol, rows in self.history.items():

            if not rows:

                continue


            if (
                now - rows[0]["time"]
                >= HISTORY_SECONDS
            ):

                ready += 1


        return {

            "symbols":
                total,

            "ready":
                ready

        }