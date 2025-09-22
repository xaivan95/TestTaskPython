import json
import shutil
from pathlib import Path
from typing import List
from .logger import timed_step, BuildLogger
from .config import BuildConfig

class FileProcessor:
    def __init__(self, config: BuildConfig):
        self.config = config
        self.logger = BuildLogger()

    @timed_step("Обработка исходного кода")
    def process(self, repo_path: Path) -> Path:
        source_dir = self._find_source_directory(repo_path, self.config.source_path)

        if not source_dir or not source_dir.exists():
            available_paths = [str(p.relative_to(repo_path)) for p in repo_path.rglob('*') if p.is_dir()]
            raise FileNotFoundError(
                f"Директория с исходным кодом не найдена: {self.config.source_path}\n"
                f"Доступные пути: {available_paths}"
            )

        self.logger.log_step(f"Найдена директория с исходным кодом: {source_dir}")

        work_dir = self._prepare_working_directory(source_dir)

        self._create_version_file(work_dir)

        return work_dir

    def _find_source_directory(self, repo_path: Path, source_path: str) -> Path:
        possible_paths = [
            repo_path / source_path,
            repo_path / source_path.replace('/', '\\'),  # Для Windows
            *[p for p in repo_path.rglob('*') if p.name == Path(source_path).name and p.is_dir()]
        ]

        for path in possible_paths:
            if path.exists():
                return path

        return None

    def _prepare_working_directory(self, source_dir: Path) -> Path:
        work_dir = Path("build_output") / source_dir.name
        if work_dir.exists():
            shutil.rmtree(work_dir)

        shutil.copytree(source_dir, work_dir)
        self.logger.log_step(f"Создана рабочая директория: {work_dir}")

        return work_dir

    def _create_version_file(self, source_dir: Path) -> None:
        self.logger.log_step("Создание version.json")

        source_files = self._find_source_files(source_dir)

        version_data = {
            "name": "hello world",
            "version": self.config.version,
            "files": sorted(source_files)
        }

        version_file_path = source_dir / "version.json"

        try:
            with open(version_file_path, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, ensure_ascii=False, indent=2)

            self.logger.log_step(f"Создан version.json с {len(source_files)} файлами в атрибуте FILES: {source_files}")
        except Exception as e:
            raise Exception(f"Ошибка создания version.json: {e}")

    def _find_source_files(self, directory: Path) -> List[str]:
        files = []

        for ext in self.config.allowed_extensions:
            for file_path in directory.rglob(f"*{ext}"):
                if file_path.is_file() and file_path.name != "version.json":
                    # Сохраняем относительный путь
                    relative_path = file_path.relative_to(directory)
                    files.append(str(relative_path).replace('\\', '/'))  # Унифицируем разделители

        return files


class DirectoryValidator:
    @staticmethod
    @timed_step("Валидация структуры")
    def validate_source_structure(source_dir: Path) -> bool:
        logger = BuildLogger()

        if not source_dir.exists():
            raise ValueError(f"Директория не существует: {source_dir}")

        files = list(source_dir.rglob('*'))
        if not files:
            raise ValueError(f"Директория пуста: {source_dir}")

        source_files = [f for f in files if f.is_file() and f.suffix in ('.py', '.js', '.sh')]
        logger.log_step(f"Найдено {len(source_files)} исходных файлов")

        logger.log_step("Структура директории валидна")
        return True