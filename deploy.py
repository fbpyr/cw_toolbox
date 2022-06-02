import datetime
import shutil
import sys
from pathlib import Path
from configparser import ConfigParser

from watchgod import watch, RegExpWatcher


def ensure_availability(source: Path, destination: Path):
    if not source.exists():
        print(f"could not find {source} - aborting")
        sys.exit(1)
    if not destination.exists():
        print(f"could not find {source} - creating dir")
        destination.mkdir(parents=True, exist_ok=True)


def get_destination_path_from_matching_roots(source: Path, destination: Path, root_match: str) -> Path:
    if source.parent.name == destination.name:
        destination = destination / source.name
        #print(f"dirs match! destination correct: {destination =}")
        return destination
    sub_dir_names = []
    for sub_path in source.parents:
        if sub_path.name == root_match:
            #print(f"found lib_root: {sub_path}")
            break
        sub_dir_names.append(sub_path.name)
    #print(f"{sub_dir_names =}")
    for dir_name in sub_dir_names:
        destination = destination / dir_name
    destination.mkdir(parents=True, exist_ok=True)
    return destination / source.name


def get_change_info(change) -> (str, Path):
    change_set = next(iter(change))
    change_category, change_file = change_set
    return change_category.name, Path(next(iter(change))[1])


def deploy_to(source: Path, destination: Path):
    shutil.copy(source, destination)


SOURCE = Path(__file__).parent
SOURCE_DIR_NAME = SOURCE.name
targets = [
    Path("c:/programdata/lib/python/3.8/virtualenvs/cadwork/Lib/site-packages/cw_toolbox"),
]

config_file = Path(__file__).parent / 'config.ini'
if config_file.exists():
    config = ConfigParser()
    config.read(config_file)

    user_home = str(Path().home().absolute())

    for section in ["additional_deploy_paths"]:
        for opt in config.options(section):
            additional_deploy_path = Path(config.get(section, opt).format(user_home=user_home))
            print(section, opt, additional_deploy_path)
            targets.append(additional_deploy_path)

for target in targets:
    ensure_availability(SOURCE, target)


WATCH_EXTENSION = "py"
WATCH_RE = {"re_files": f"^.*(\\.{WATCH_EXTENSION})$"}

print(f"\nINFO: {datetime.datetime.now().isoformat()} now watching for changes in {SOURCE}")
for changes in watch(SOURCE, watcher_cls=RegExpWatcher, watcher_kwargs=WATCH_RE):
    change_type, source_file_path = get_change_info(changes)
    print(f"detected change {change_type}: {source_file_path}")

    if change_type == "modified" or change_type == "added":
        for target in targets:
            target_file_path = get_destination_path_from_matching_roots(source_file_path, target, SOURCE_DIR_NAME)
            path_max_len = max([len(str(source_file_path)), len(str(target_file_path))])
            print(str(source_file_path).rjust(path_max_len + 2))
            print(str(target_file_path).rjust(path_max_len + 2))
            deploy_to(source=source_file_path, destination=target_file_path)
            print(f"INFO: {datetime.datetime.now().isoformat()} deployed successfully to: {target}")

    elif change_type == "deleted":
        for target in targets:
            target_file_path = get_destination_path_from_matching_roots(source_file_path, target, SOURCE_DIR_NAME)
            path_max_len = max([len(str(source_file_path)), len(str(target_file_path))])
            print(str(source_file_path).rjust(path_max_len + 2))
            print(str(target_file_path).rjust(path_max_len + 2))
            target_file_path.unlink(missing_ok=True)
            print(f"INFO: {datetime.datetime.now().isoformat()} removed successfully from: {target}")

    print()
