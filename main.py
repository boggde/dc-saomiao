import time


from config import (
    SCAN_INTERVAL,
    WEB_HOST,
    WEB_PORT,
    MIN_24H_VOLUME
)


from binance_client import BinanceClient

from storage import Storage

from detector import Detector

from telegram import Telegram

from web import (
    start_web,
    update_alerts
)



def main():


    print(
        "Starting Binance Anomaly Monitor V1..."
    )



    client = BinanceClient()


    # -----------------------------
    # Health Check
    # -----------------------------

    if not client.health_check():

        print(
            "Binance unavailable. Exit."
        )

        return

    valid_symbols = (
        client.get_perpetual_symbols()
    )

    print(
        "[READY] Binance connection OK"
    )



    storage = Storage()


    detector = Detector()


    telegram = Telegram()


    # =============================
    # Telegram启动测试
    # =============================

    telegram.startup_test()



    start_web(
        WEB_HOST,
        WEB_PORT
    )


    print(
        f"[WEB] http://{WEB_HOST}:{WEB_PORT}"
    )


    print(
        "[RUNNING]"
    )



    alerts_cache = {}



    while True:


        try:


            tickers = (
                client.get_tickers()
            )



            now_alerts = []
            active_symbols = 0

            for item in tickers:

                symbol = item.get(
                    "symbol"
                )

                if symbol not in valid_symbols:
                    continue

                volume_24h = float(
                    item.get(
                        "quoteVolume",
                        0
                    )
                )

                if volume_24h < MIN_24H_VOLUME:
                    continue

                price = item.get(
                    "lastPrice"
                )

                if not price or not volume_24h:
                    continue


                active_symbols += 1


                storage.add(

                    symbol,

                    price,

                    volume_24h

                )



                history = storage.get(
                    symbol
                )



                result = detector.analyze(

                    symbol,

                    history

                )



                if not result:

                    continue



                if result["signal"]:


                    now_alerts.append(
                        result
                    )



                    if not detector.in_cooldown(
                        symbol
                    ):


                        text = (
                            telegram
                            .format_alert(
                                result
                            )
                        )


                        success = (
                            telegram.send(
                                text
                            )
                        )



                        if success:

                            detector.set_cooldown(
                                symbol
                            )

                            print(
                                f"[ALERT SENT] {symbol}"
                            )


                        else:

                            print(
                                f"[ALERT FAILED] {symbol}"
                            )



            update_alerts(
                now_alerts
            )


            status = storage.status()


            print(
                f"[SCAN OK] "
                f"Futures={len(valid_symbols)} "
                f"Active={active_symbols} "
                f"Cached={status['symbols']} "
                f"Ready={status['ready']} "
                f"Alerts={len(now_alerts)}"
            )



            time.sleep(
                SCAN_INTERVAL
            )



        except KeyboardInterrupt:


            print(
                "Stopped."
            )

            break



        except Exception as e:


            print(
                "[MAIN ERROR]",
                type(e).__name__,
                e
            )


            time.sleep(
                5
            )





if __name__ == "__main__":

    main()
