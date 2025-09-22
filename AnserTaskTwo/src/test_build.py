import sys
from pathlib import Path
from DownloadSystem import ConfigFactory
from src.main import BuildOrchestrator

sys.path.insert(0, str(Path(__file__).parent))

def test_build():
    """Тестовая сборка"""
    config = ConfigFactory.create_from_args(
        "https://github.com/paulbouwer/hello-kubernetes",
        "src/app",
        "25.3000"
    )

    orchestrator = BuildOrchestrator(config)
    success = orchestrator.run()

    if success:
        print("Сборка завершена успешно!")
    else:
        print("Сборка завершена с ошибками!")


if __name__ == "__main__":
    test_build()