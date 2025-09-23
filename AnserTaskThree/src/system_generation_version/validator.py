import re
from typing import List
from pathlib import Path


class ConfigValidator:
    @staticmethod
    def validate_version_format(version: str) -> bool:
        if not version:
            return False

        pattern = r'^\d+(\.\d+)*$'
        return bool(re.match(pattern, version))

    @staticmethod
    def validate_template(template: str) -> bool:
        if not template:
            return False

        pattern = r'^[\d\*]+(\.[\d\*]+)*$'
        if not re.match(pattern, template):
            return False

        return '*' in template

    @staticmethod
    def validate_config_file(config_path: Path) -> bool:
        return config_path.exists() and config_path.is_file()


class VersionValidator:
    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        v1_parts = list(map(int, version1.split('.')))
        v2_parts = list(map(int, version2.split('.')))

        max_length = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_length - len(v1_parts)))
        v2_parts.extend([0] * (max_length - len(v2_parts)))

        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1

        return 0

    @staticmethod
    def normalize_version(version: str, target_length: int) -> List[int]:
        parts = list(map(int, version.split('.')))
        if len(parts) < target_length:
            parts.extend([0] * (target_length - len(parts)))
        return parts