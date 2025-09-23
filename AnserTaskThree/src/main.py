import argparse
import sys
from pathlib import Path
from typing import Dict, List
from system_generation_version import (
    ConfigParser, VersionGenerator, VersionSorter,
    VersionFilter, VersionFormatter, ConfigValidator
)

sys.path.insert(0, str(Path(__file__).parent))

class VersionManager:
    def __init__(self, target_version: str, config_path: Path):
        self.target_version = target_version
        self.config_path = config_path
        self.validator = ConfigValidator()

    def run(self) -> bool:
        try:
            self._validate_input()

            print("=" * 60)
            print("ГЕНЕРАТОР списка ВЕРСИЙ")
            print("=" * 60)
            print(f"Целевая версия: {self.target_version}")
            print(f"Конфигурационный файл: {self.config_path}")
            print()

            templates = self._parse_configuration()
            print(f"Загружено шаблонов: {len(templates)}")

            template_results = self._generate_versions(templates)

            all_versions = self._collect_all_versions(template_results)
            print(f"Сгенерировано уникальных версий: {len(all_versions)}")
            print()

            sorted_versions = VersionSorter.sort_versions(all_versions)
            print(VersionFormatter.format_version_list(sorted_versions, "Все версии (отсортированные)"))
            print()

            version_filter = VersionFilter(self.target_version)
            older_versions = version_filter.filter_older_versions(all_versions)

            print(VersionFormatter.format_version_list(older_versions, f"Версии старше {self.target_version}"))
            print()

            self._print_statistics(all_versions, version_filter)

            print("=" * 60)
            print("ВЫПОЛНЕНИЕ ЗАВЕРШЕНО")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"❌ ОШИБКА: {e}")
            return False

    def _validate_input(self) -> None:
        if not self.validator.validate_version_format(self.target_version):
            raise ValueError(f"Неверный формат версии: {self.target_version}")

        if not self.validator.validate_config_file(self.config_path):
            raise FileNotFoundError(f"Конфигурационный файл не найден: {self.config_path}")

    def _parse_configuration(self) -> Dict[str, str]:
        parser = ConfigParser()
        return parser.parse_config(self.config_path)

    def _generate_versions(self, templates: Dict[str, str]) -> Dict[str, List[str]]:
        generator = VersionGenerator()
        results = generator.generate_versions_from_templates(templates)
        print(VersionFormatter.format_template_results(results))
        print()

        return results

    def _collect_all_versions(self, template_results: Dict[str, List[str]]) -> List[str]:
        all_versions = set()

        for versions in template_results.values():
            all_versions.update(versions)

        return list(all_versions)

    def _print_statistics(self, all_versions: List[str], version_filter: VersionFilter) -> None:
        groups = version_filter.group_versions_by_age(all_versions)

        print("СТАТИСТИКА:")
        print(f"  Всего версий: {len(all_versions)}")
        print(f"  Старше целевой: {len(groups['older'])}")
        print(f"  Равны целевой: {len(groups['equal'])}")
        print(f"  Новее целевой: {len(groups['newer'])}")

        if all_versions:
            min_version = VersionSorter.sort_versions(all_versions)[0]
            max_version = VersionSorter.sort_versions_desc(all_versions)[0]
            print(f"  Самая старая: {min_version}")
            print(f"  Самая новая: {max_version}")


def main():
    parser = argparse.ArgumentParser(description='Генератор версий на основе шаблонов')
    parser.add_argument('version', help='Целевая версия (например: 2.1.0)')
    parser.add_argument('config', help='Путь к конфигурационному файлу')

    args = parser.parse_args()

    config_path = Path(args.config)

    manager = VersionManager(args.version, config_path)
    success = manager.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()