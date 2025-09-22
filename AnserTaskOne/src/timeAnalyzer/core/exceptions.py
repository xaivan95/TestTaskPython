class TimeServiceError(Exception):
    """Базовая ошибка сервиса времени"""
    pass

class APIError(TimeServiceError):
    """Ошибка API"""
    pass

class ValidationError(TimeServiceError):
    """Ошибка валидации данных"""
    pass

class NetworkError(TimeServiceError):
    """Сетевая ошибка"""
    pass