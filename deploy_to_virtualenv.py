from watchgod import watch, PythonWatcher
from pathlib import Path
import datetime
import shutil
import sys


def check_availability(source: Path, destination: Path):
    for path in [source, destination]:
        if not path.exists():
            print(f"could not find {path} - aborting")
            sys.exit(1)


def deploy_to(source: Path, destination: Path):
    shutil.copytree(source, destination, dirs_exist_ok=True)


SOURCE = Path(__file__).parent
TARGET = Path().home() / ".virtualenvs" / "cadwork" / "Lib" / "site-packages" / "cw_toolbox"

print(f"\nINFO: {datetime.datetime.now().isoformat()} now watching for changes in {SOURCE}")
for changes in watch(SOURCE, watcher_cls=PythonWatcher):
    print(f"detected changes: {changes =}")
    check_availability(SOURCE, TARGET)
    deploy_to(source=SOURCE, destination=TARGET)
    print(f"\nINFO: {datetime.datetime.now().isoformat()} deployed to {TARGET} \n")
