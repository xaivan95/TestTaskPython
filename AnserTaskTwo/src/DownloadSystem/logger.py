import time
import logging
from functools import wraps
from typing import Callable, Any
from datetime import datetime


class BuildLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        self.logger = logging.getLogger('BuildScript')
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_step(self, message: str):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.logger.info(f"[{current_time}] {message}")


def timed_step(step_name: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = BuildLogger()
            start_time = time.time()
            logger.log_step(f"Начало: {step_name}")

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.log_step(f"Завершено: {step_name} (время: {execution_time:.2f}с)")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.log_step(f"Ошибка в {step_name} (время: {execution_time:.2f}с): {e}")
                raise

        return wrapper

    return decorator