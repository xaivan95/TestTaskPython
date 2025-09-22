from abc import ABC, abstractmethod
from typing import Optional
from ..core.entities import TimeData

class Formatter(ABC):
    @abstractmethod
    def format(self, time_data: TimeData, delta: Optional[float] = None) -> str:
        pass