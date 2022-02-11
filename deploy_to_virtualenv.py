from watchgod import watch, PythonWatcher
from pathlib import Path
import datetime
import shutil
import sys


def ensure_availability(source: Path, destination: Path):
    if not source.exists():
        print(f"could not find {source} - aborting")
        sys.exit(1)
    if not destination.exists():
        print(f"could not find {source} - creating dir")
        destination.mkdir(parents=True, exist_ok=True)


def get_destination_path_from_matching_roots(source: Path, destination: Path, root_match: str) -> Path:
    #print(f"{source.parent.name == destination.name} ")
    if source.parent.name == destination.name:
        destination = destination / source.name
        #print(f"dirs match! destination correct: {destination =}")
        return destination
    #print("dirs do not match!")
    sub_dir_names = []
    for sub_path in source.parents:
        #print(sub_path.name)
        if sub_path.name == root_match:
            #print(f"found lib_root: {sub_path}")
            break
        sub_dir_names.append(sub_path.name)
    #print(f"{sub_dir_names =}")
    for dir_name in sub_dir_names:
        destination = destination / dir_name
    destination.mkdir(parents=True, exist_ok=True)
    return destination / source.name


def get_change_info(change) -> (int, Path):
    change_set = next(iter(change))
    change_type, change_file = change_set
    return (change_type.name, Path(next(iter(change))[1]))


def deploy_to(source: Path, destination: Path):
    shutil.copy(source, destination)


SOURCE = Path(__file__).parent
SOURCE_DIR_NAME = SOURCE.name
TARGET = Path().home() / ".virtualenvs" / "cadwork" / "Lib" / "site-packages" / "cw_toolbox"

ensure_availability(SOURCE, TARGET)

print(f"\nINFO: {datetime.datetime.now().isoformat()} now watching for changes in {SOURCE}")
for changes in watch(SOURCE, watcher_cls=PythonWatcher):
    change_type, source_file = get_change_info(changes)
    print(f"detected change {change_type}: {source_file}")
    target_file_path = get_destination_path_from_matching_roots(source_file, TARGET, SOURCE_DIR_NAME)
    print(f"  {str(source_file).rjust(123)}")
    print(f"  {str(target_file_path).rjust(123)}")
    deploy_to(source=source_file, destination=target_file_path)
    print(f"INFO: {datetime.datetime.now().isoformat()} deployed to {TARGET} \n")
