from .implementations import RawFormatter, NORMALReadableFormatter, DeltaFormatter
from .base import Formatter
from ..core.constants import FormatterType


class FormatterFactory:
    @staticmethod
    def create(formatter_type: FormatterType) -> Formatter:
        formatters = {
            FormatterType.RAW: RawFormatter,
            FormatterType.NORMAL: NORMALReadableFormatter,
            FormatterType.DELTA: DeltaFormatter,
        }

        if formatter_type not in formatters:
            raise ValueError(f"Unknown formatter type: {formatter_type}")

        return formatters[formatter_type]()