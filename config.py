import os
from dotenv import load_dotenv


load_dotenv()


# =====================================================
# Binance
# =====================================================

BINANCE_BASE_URL = os.getenv(
    "BINANCE_BASE_URL",
    "https://fapi.binance.com"
)


# =====================================================
# Scanner
# =====================================================

# 扫描间隔 秒
SCAN_INTERVAL = int(
    os.getenv(
        "SCAN_INTERVAL",
        "5"
    )
)


# 保存历史时间
HISTORY_SECONDS = 3600


# =====================================================
# Market Filter
# =====================================================

# 最低24小时成交额 USDT

MIN_24H_VOLUME = int(
    os.getenv(
        "MIN_24H_VOLUME",
        "5000000"
    )
)


# =====================================================
# Signal
# =====================================================

# 1小时振幅阈值 %

RANGE_THRESHOLD = float(
    os.getenv(
        "RANGE_THRESHOLD",
        "10"
    )
)


# Telegram冷却时间

ALERT_COOLDOWN_SECONDS = int(
    os.getenv(
        "ALERT_COOLDOWN_SECONDS",
        "3600"
    )
)


# =====================================================
# Retry
# =====================================================

RETRY_SEQUENCE = [
    2,
    4,
    8
]


REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "10"
    )
)


# =====================================================
# Binance Safety
# =====================================================

MAX_WEIGHT_PER_MINUTE = 1920


FATAL_STATUS_CODES = [
    418,
    429
]


# =====================================================
# Telegram
# =====================================================

TELEGRAM_ENABLED = (
    os.getenv(
        "TELEGRAM_ENABLED",
        "true"
    ).lower()
    == "true"
)


TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    ""
)


TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)


# =====================================================
# Web
# =====================================================

# Docker必须监听0.0.0.0

WEB_HOST = os.getenv(
    "WEB_HOST",
    "0.0.0.0"
)


WEB_PORT = int(
    os.getenv(
        "WEB_PORT",
        "8080"
    )
)


# =====================================================
# Storage
# =====================================================

DATA_PATH = os.getenv(
    "DATA_PATH",
    "/app/data"
)