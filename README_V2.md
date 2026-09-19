# Coin Scanner V2

REST-only Binance USDⓈ-M Futures scanner.

## Run

```bash
pip install -r requirements.txt
python scanner.py
```

Web UI:

http://127.0.0.1:8080

## REST safety

- No WebSocket.
- Timeout/network/5xx: retry 2s -> 4s -> 8s, max 3 retries.
- HTTP 429: immediate process exit.
- HTTP 418: immediate process exit.
- Local REQUEST_WEIGHT ceiling: 80% of 2400/min = 1920/min.
- Maximum HTTP concurrency: 10.
- Proxy is controlled by BINANCE_PROXY in .env.

## Scheduling

- Level 1: every 60s, offset 0s.
- Level 2: every 30s, offset 3s.
- Level 3: every 10s, offset 1s.
- Top 3 is derived from Top 10 and does not create extra Binance requests.

## Current steady-state planned weight

- L1 ticker: 40/min.
- L2: 50 symbols x 1 weight x 2/min = 100/min.
- L3 klines: 10 x 3 x 2 x 6 = 360/min.
- L3 depth: 10 x 5 x 6 = 300/min.
- L3 open interest: 10 x 1 x 6 = 60/min.
- L3 mark/funding: 10 x 1 x 6 = 60/min.

Nominal steady-state total: 920 weight/min.

This is the planned scanner request budget before retries. Retry traffic is exceptional and is not included in the steady-state figure.
