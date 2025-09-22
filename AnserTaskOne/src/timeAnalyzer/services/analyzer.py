import asyncio
from typing import List
import time
from .timeService import TimeService
from ..config.settings import settings
from ..core.entities import  AnalysisResult, SeriesResult
from ..core.exceptions import TimeServiceError
from ..core.constants import TimeConstants


class TimeAnalyzer:
    def __init__(self, time_service: TimeService):
        self.time_service = time_service

    async def calculate_time_delta(self, geo: str) -> AnalysisResult:
        local_start_time = time.time() * TimeConstants.MS_IN_SECOND

        time_data, request_time = await self.time_service.fetch_time_data(geo)

        clock_data = time_data.raw_data['clocks'].get(geo, {})
        offset_ms = clock_data.get('offset', 0)

        api_time_with_offset = time_data.timestamp
        local_time_with_offset = local_start_time + offset_ms

        delta = abs(api_time_with_offset - local_time_with_offset) + request_time

        return AnalysisResult(
            time_data=time_data,
            delta_ms=delta,
            request_duration_ms=request_time
        )

    async def run_series_analysis(self, geo: str, num_requests: int = None) -> SeriesResult:
        if num_requests is None:
            num_requests = TimeConstants.DEFAULT_SERIES_SIZE

        deltas: List[float] = []

        for i in range(num_requests):
            try:
                result = await self.calculate_time_delta(geo)
                deltas.append(result.delta_ms)
                print(f"Запрос {i + 1}: дельта = {result.delta_ms:.3f} мс")

                if i < num_requests - 1:
                    await asyncio.sleep(settings.REQUEST_DELAY)

            except TimeServiceError as e:
                print(f"Ошибка в запросе {i + 1}: {e}")
                deltas.append(float('inf'))

        successful_deltas = [d for d in deltas if d != float('inf')]

        if not successful_deltas:
            raise TimeServiceError("Все запросы завершились ошибкой")

        average_delta = sum(successful_deltas) / len(successful_deltas)

        return SeriesResult(
            deltas=deltas,
            average_delta=average_delta,
            successful_requests=len(successful_deltas),
            total_requests=num_requests
        )