import shutil

import requests
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from .logger import timed_step, BuildLogger
from .config import BuildConfig


class RepositoryDownloader:
    def __init__(self, config: BuildConfig):
        self.config = config
        self.logger = BuildLogger()

    @timed_step("Загрузка репозитория")
    def download(self) -> Path:
        if "github.com" in self.config.repository_url:
            return self._download_github()
        else:
            return self._download_generic()

    def _download_github(self) -> Path:
        repo_url = self.config.repository_url
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]

        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) >= 2:
            owner, repo_name = path_parts[0], path_parts[1]
            branches = ['main', 'master', 'develop']

            for branch in branches:
                archive_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/{branch}.zip"
                self.logger.log_step(f"Попытка загрузки с ветки: {branch}")

                try:
                    response = requests.get(archive_url, stream=True, timeout=30)
                    if response.status_code == 200:
                        return self._download_and_extract(archive_url, repo_name)
                except requests.RequestException:
                    continue

            raise Exception(f"Не удалось загрузить репозиторий. Проверьте URL: {repo_url}")
        else:
            raise Exception(f"Некорректный URL репозитория: {repo_url}")

    def _download_and_extract(self, archive_url: str, repo_name: str) -> Path:
        self.logger.log_step(f"Загрузка архива: {archive_url}")

        response = requests.get(archive_url, stream=True, timeout=30)
        response.raise_for_status()

        temp_dir = Path(self.config.temp_dir)
        temp_dir.mkdir(exist_ok=True)

        zip_path = temp_dir / "repo.zip"

        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        self.logger.log_step("Архив загружен, распаковка...")

        extract_path = temp_dir / "extracted"
        if extract_path.exists():
            shutil.rmtree(extract_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        contents = list(extract_path.iterdir())
        if contents:
            if len(contents) == 1 and contents[0].is_dir():
                repo_dir = contents[0]
                self.logger.log_step(f"Репоизторий распакован в: {repo_dir}")
                return repo_dir
            else:
                self.logger.log_step(f"Найдено несколько элементов: {[c.name for c in contents]}")
                return extract_path

        raise Exception("Не удалось найти распакованный репозиторий")

    def _download_generic(self) -> Path:
        raise NotImplementedError("Поддерживается только GitHub")