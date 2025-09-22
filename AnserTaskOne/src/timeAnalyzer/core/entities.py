from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass(frozen=True)
class TimeData:
    timestamp: int
    timezone_name: str
    offset_string: str
    raw_data: Dict[str, Any]

@dataclass
class AnalysisResult:
    time_data: TimeData
    delta_ms: float
    request_duration_ms: float

@dataclass
class SeriesResult:
    deltas: List[float]
    average_delta: float
    successful_requests: int
    total_requests: int