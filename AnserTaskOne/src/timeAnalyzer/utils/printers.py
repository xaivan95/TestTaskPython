from typing import Optional
from ..core.entities import TimeData
from ..core.constants import FormatterType
from ..formatters.factory import FormatterFactory

class ResultPrinter:
    def __init__(self):
        self.formatter_factory = FormatterFactory()

    def print_section(self, title: str, width: int = 60):
        print(f"\n{'=' * width}")
        print(f"{title:^{width}}")
        print(f"{'=' * width}")

    def print_result(self, title: str, formatter_type: FormatterType,
                     time_data: TimeData, delta: Optional[float] = None):
        """Печать результата"""
        formatter = self.formatter_factory.create(formatter_type)
        self.print_section(title)
        print(formatter.format(time_data, delta))