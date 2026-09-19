import time
import requests

from config import (
    BINANCE_BASE_URL,
    REQUEST_TIMEOUT,
    RETRY_SEQUENCE,
    FATAL_STATUS_CODES
)


class BinanceClient:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "AnomalyMonitor-V1"
            }
        )

        # ===============================
        # 强制关闭系统代理
        # ===============================
        self.session.trust_env = False


    # ============================================
    # 获取USDT永续白名单
    # ============================================

    def get_perpetual_symbols(self):

        data = self.get(
            "/fapi/v1/exchangeInfo"
        )

        symbols = set()

        for item in data.get(
            "symbols",
            []
        ):

            if (
                item.get("contractType") == "PERPETUAL"
                and
                item.get("quoteAsset") == "USDT"
                and
                item.get("status") == "TRADING"
            ):

                symbols.add(
                    item["symbol"]
                )


        print(
            f"[SYMBOL FILTER] "
            f"{len(symbols)} USDT perpetual symbols"
        )


        return symbols


    # ============================================
    # 通用GET
    # ============================================

    def get(self, endpoint):

        url = (
            BINANCE_BASE_URL
            +
            endpoint
        )


        for index, delay in enumerate(
            [0] + RETRY_SEQUENCE
        ):

            if delay:
                time.sleep(delay)


            try:

                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT
                )


                if response.status_code in FATAL_STATUS_CODES:

                    print(
                        f"[FATAL] Binance status {response.status_code}"
                    )

                    raise SystemExit(
                        "Binance rate limit protection triggered"
                    )


                response.raise_for_status()


                return response.json()



            except Exception as e:


                print(
                    f"[REQUEST ERROR] {endpoint}: "
                    f"{type(e).__name__}: {e}"
                )


                if index >= len(RETRY_SEQUENCE):

                    raise


        return None



    # ============================================
    # Health Check
    # ============================================

    def health_check(self):

        print(
            "[HEALTH] Checking Binance connection..."
        )


        for i, delay in enumerate(
            [0] + RETRY_SEQUENCE
        ):


            if delay:

                print(
                    f"[RETRY] Health check retry {i}/3 in {delay}s"
                )

                time.sleep(delay)



            try:

                data = self.get(
                    "/fapi/v1/ping"
                )


                if data == {}:

                    print(
                        "[HEALTH OK] Binance REST reachable"
                    )

                    return True



            except Exception:

                pass



        print(
            "[HEALTH FAILED] Binance unavailable"
        )

        return False



    # ============================================
    # 获取全部24hr ticker
    # ============================================

    def get_tickers(self):

        return self.get(
            "/fapi/v1/ticker/24hr"
        )