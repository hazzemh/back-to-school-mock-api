from datetime import datetime
from zoneinfo import ZoneInfo

RIYADH = ZoneInfo("Asia/Riyadh")


def now_riyadh() -> datetime:
    return datetime.now(tz=RIYADH)
