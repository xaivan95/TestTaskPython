import asyncio
from typing import Dict, Any
import aiohttp
from aiohttp import ClientSession
from ..config.settings import settings
from ..core.entities import TimeData
from ..core.exceptions import APIError, ValidationError, NetworkError
from ..http.decorators import timing_decorator


class TimeService:
    def __init__(self, session: ClientSession):
        self.session = session

    @timing_decorator
    async def fetch_time_data(self, geo: str) -> TimeData:
        url = f"{settings.BASE_URL}?geo={geo}"

        for attempt in range(settings.RETRY_ATTEMPTS):
            try:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    if not self._validate_time_data(data):
                        raise ValidationError("Некорректные данные от API")

                    return self._parse_time_data(data, geo)

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == settings.RETRY_ATTEMPTS - 1:
                    raise NetworkError(f"Network error after {settings.RETRY_ATTEMPTS} attempts: {e}")
                await asyncio.sleep(1 * (attempt + 1))

    def _validate_time_data(self, data: Dict[str, Any]) -> bool:
        return (
                isinstance(data, dict) and
                'time' in data and
                'clocks' in data and
                isinstance(data['time'], (int, float))
        )

    def _parse_time_data(self, data: Dict[str, Any], geo: str) -> TimeData:
        clock_data = data['clocks'].get(geo, {})
        return TimeData(
            timestamp=data['time'],
            timezone_name=clock_data.get('name', 'Неизвестно'),
            offset_string=clock_data.get('offsetString', 'Неизвестно'),
            raw_data=data
        )