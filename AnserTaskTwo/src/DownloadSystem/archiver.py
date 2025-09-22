import zipfile
import shutil
from pathlib import Path
from .logger import timed_step, BuildLogger
from .config import BuildConfig


class ArchiveBuilder:
    def __init__(self, config: BuildConfig):
        self.config = config
        self.logger = BuildLogger()

    @timed_step("Создание архива")
    def build_archive(self, source_dir: Path) -> Path:
        archive_path = Path(self.config.archive_name)

        if archive_path.exists():
            archive_path.unlink()

        self.logger.log_step(f"Создание архива: {archive_path}")

        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source_dir)
                        zipf.write(file_path, arcname)
                        self.logger.log_step(f"Добавлен в архив: {arcname}")

            archive_size = archive_path.stat().st_size / 1024  # KB
            self.logger.log_step(f"Архив создан: {archive_path} ({archive_size:.1f} KB)")
            return archive_path

        except Exception as e:
            if archive_path.exists():
                archive_path.unlink()
            raise Exception(f"Ошибка создания архива: {e}")


class CleanupManager:
    def __init__(self, config: BuildConfig):
        self.config = config
        self.logger = BuildLogger()

    @timed_step("Очистка временных файлов")
    def cleanup(self) -> None:
        temp_dirs = [Path("temp_build"), Path("build_output")]

        for temp_dir in temp_dirs:
            if temp_dir.exists() and temp_dir.is_dir():
                try:
                    shutil.rmtree(temp_dir)
                    self.logger.log_step(f"Удалена временная директория: {temp_dir}")
                except Exception as e:
                    self.logger.log_step(f"Ошибка удаления {temp_dir}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()