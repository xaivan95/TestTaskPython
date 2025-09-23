import json
from pathlib import Path
from typing import Dict, Any
from .validator import ConfigValidator

class ConfigParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def parse_config(self, config_path: Path) -> Dict[str, str]:
        if not ConfigValidator.validate_config_file(config_path):
            raise FileNotFoundError(f"Конфигурационный файл не найден: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            return self._validate_config_data(config_data)

        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Ошибка чтения конфигурации: {e}")

    def _validate_config_data(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        if not isinstance(config_data, dict):
            raise ValueError("Конфигурация должна быть словарем")

        validated_config = {}

        for key, template in config_data.items():
            if not isinstance(template, str):
                raise ValueError(f"Шаблон для {key} должен быть строкой")

            if not ConfigValidator.validate_template(template):
                raise ValueError(f"Неверный формат шаблона {key}: {template}")

            validated_config[key] = template

        if not validated_config:
            raise ValueError("Конфигурационный файл пуст")

        return validated_config