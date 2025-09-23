from typing import List, Dict
from .validator import VersionValidator


class VersionSorter:
    @staticmethod
    def sort_versions(versions: List[str]) -> List[str]:
        return sorted(versions, key=lambda v: [int(part) for part in v.split('.')])

    @staticmethod
    def sort_versions_desc(versions: List[str]) -> List[str]:
        return sorted(versions, key=lambda v: [int(part) for part in v.split('.')], reverse=True)

class VersionFilter:
    def __init__(self, target_version: str):
        self.target_version = target_version
        self.validator = VersionValidator()

    def filter_older_versions(self, versions: List[str]) -> List[str]:
        older_versions = []

        for version in versions:
            if self.validator.compare_versions(version, self.target_version) == -1:
                older_versions.append(version)

        return older_versions

    def filter_newer_versions(self, versions: List[str]) -> List[str]:
        newer_versions = []

        for version in versions:
            if self.validator.compare_versions(version, self.target_version) == 1:
                newer_versions.append(version)

        return newer_versions

    def group_versions_by_age(self, versions: List[str]) -> Dict[str, List[str]]:
        older = self.filter_older_versions(versions)
        newer = self.filter_newer_versions(versions)
        equal = [v for v in versions if self.validator.compare_versions(v, self.target_version) == 0]

        return {
            'older': older,
            'equal': equal,
            'newer': newer
        }


class VersionFormatter:

    @staticmethod
    def format_version_list(versions: List[str], title: str) -> str:
        if not versions:
            return f"{title}:\n  (пусто)"

        result = [f"{title} ({len(versions)} версий):"]
        for i, version in enumerate(versions, 1):
            result.append(f"  {i:2d}. {version}")

        return '\n'.join(result)

    @staticmethod
    def format_template_results(template_results: Dict[str, List[str]]) -> str:
        result = ["Сгенерированные версии по шаблонам:"]

        for template_name, versions in template_results.items():
            result.append(f"\n{template_name}:")
            for i, version in enumerate(versions, 1):
                result.append(f"  Вариант {i}: {version}")

        return '\n'.join(result)