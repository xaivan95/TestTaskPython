from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass(frozen=True)
class BuildConfig:
    repository_url: str
    source_path: str
    version: str
    temp_dir: Path = Path("temp_build")
    allowed_extensions: tuple = ('.py', '.js', '.sh', '.json')

    @property
    def archive_name(self) -> str:
        dir_name = Path(self.source_path).name
        date_str = datetime.now().strftime("%d%m%Y")
        return f"{dir_name}{date_str}.zip"

    def validate(self) -> None:
        if not self.repository_url:
            raise ValueError("URL репозитория не может быть пустым")
        if not self.source_path:
            raise ValueError("Путь к исходному коду не может быть пустым")
        if not self.version:
            raise ValueError("Версия не может быть пустой")


class ConfigFactory:
    @staticmethod
    def create_from_args(repo_url: str, source_path: str, version: str) -> BuildConfig:
        return BuildConfig(
            repository_url=repo_url,
            source_path=source_path,
            version=version
        )