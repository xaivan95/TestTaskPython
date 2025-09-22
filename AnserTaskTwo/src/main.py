import argparse
import sys
from pathlib import Path
from DownloadSystem import (
    RepositoryDownloader, FileProcessor, ArchiveBuilder,
    CleanupManager, ConfigFactory, BuildLogger, DirectoryValidator
)

sys.path.insert(0, str(Path(__file__).parent))

class BuildOrchestrator:
    def __init__(self, config):
        self.config = config
        self.logger = BuildLogger()

    def run(self) -> bool:
        try:
            self.logger.log_step("=" * 60)
            self.logger.log_step("ЗАПУСК ПРОЦЕССА СБОРКИ")
            self.logger.log_step("=" * 60)

            self.config.validate()

            with CleanupManager(self.config):
                downloader = RepositoryDownloader(self.config)
                repo_path = downloader.download()

                processor = FileProcessor(self.config)
                source_dir = processor.process(repo_path)

                DirectoryValidator.validate_source_structure(source_dir)

                archiver = ArchiveBuilder(self.config)
                archive_path = archiver.build_archive(source_dir)

                self.logger.log_step("=" * 60)
                self.logger.log_step(f"СБОРКА УСПЕШНО ЗАВЕРШЕНА!")
                self.logger.log_step(f"Архив создан: {archive_path}")
                self.logger.log_step("=" * 60)

                return True

        except Exception as e:
            self.logger.log_step(f"ОШИБКА СБОРКИ: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Универсальный сборщик')
    parser.add_argument('repository', help='URL репозитория')
    parser.add_argument('source_path', help='Относительный путь к исходному коду')
    parser.add_argument('version', help='Версия продукта')

    args = parser.parse_args()

    config = ConfigFactory.create_from_args(
        args.repository,
        args.source_path,
        args.version
    )

    orchestrator = BuildOrchestrator(config)
    success = orchestrator.run()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()