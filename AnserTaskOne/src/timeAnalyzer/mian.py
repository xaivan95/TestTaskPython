import asyncio
import sys
from src.timeAnalyzer.services.timeService import TimeService
from src.timeAnalyzer.config.settings import settings
from src.timeAnalyzer.core.constants import FormatterType
from src.timeAnalyzer.core.exceptions import TimeServiceError
from src.timeAnalyzer.http.client import create_http_client
from src.timeAnalyzer.services.analyzer import TimeAnalyzer
from src.timeAnalyzer.utils.printers import ResultPrinter


async def main() -> int:
    printer = ResultPrinter()

    try:
        async with create_http_client(settings.TIMEOUT_SECONDS) as session:
            time_service = TimeService(session)
            analyzer = TimeAnalyzer(time_service)

            # a) Сырой вывод данных
            result_a = await analyzer.calculate_time_delta(settings.DEFAULT_GEO)
            printer.print_result("a) Сырые данные от API", FormatterType.RAW, result_a.time_data)

            # b) "Человекопонятный" формат
            printer.print_result("b) Время в 'человекопонятном' формате", FormatterType.NORMAL, result_a.time_data)

            # c) Дельта времени для одного запроса
            result_c = await analyzer.calculate_time_delta(settings.DEFAULT_GEO)
            printer.print_result("c) Дельта времени", FormatterType.DELTA, result_c.time_data, result_c.delta_ms)

            # d) Серия запросов
            printer.print_section("d) Серия из пяти запросов")
            series_result = await analyzer.run_series_analysis(settings.DEFAULT_GEO, 5)

            print(f"\nУспешных запросов: {series_result.successful_requests}/5")
            print(f"Средняя дельта времени: {series_result.average_delta:.3f} мс")

            if series_result.successful_requests > 1:
                min_delta = min(d for d in series_result.deltas if d != float('inf'))
                max_delta = max(d for d in series_result.deltas if d != float('inf'))
                print(f"Минимальная дельта: {min_delta:.3f} мс")
                print(f"Максимальная дельта: {max_delta:.3f} мс")

    except TimeServiceError as e:
        print(f"Ошибка приложения: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nПриложение прервано пользователем")
        return 130
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return 1

    return 0

def run():
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

if __name__ == "__main__":
    run()