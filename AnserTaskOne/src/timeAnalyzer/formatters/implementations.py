import json
from datetime import datetime, timezone
from typing import Optional
from .base import Formatter
from ..core.entities import TimeData

class RawFormatter(Formatter):
    def format(self, time_data: TimeData, delta: Optional[float] = None) -> str:
        return json.dumps(time_data.raw_data, ensure_ascii=False, indent=2)

class NORMALReadableFormatter(Formatter):
    def format(self, time_data: TimeData, delta: Optional[float] = None) -> str:
        dt = datetime.fromtimestamp(time_data.timestamp / 1000, tz=timezone.utc)
        NORMAL_time = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return (f"Время: {NORMAL_time}\n"
                f"Временная зона: {time_data.timezone_name} ({time_data.offset_string})")

class DeltaFormatter(Formatter):
    def format(self, time_data: TimeData, delta: Optional[float] = None) -> str:
        if delta is None:
            return "Дельта не рассчитана"
        return f"Дельта времени: {delta:.3f} мс"