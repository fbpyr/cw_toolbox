import sys
import configparser
from pathlib import Path


def get_cw_version_info():
    """
    Retrieves cw version information from build.ini
    :return:
    """
    cw_exe = Path(sys.executable)
    cw_version_ini = cw_exe.parent / "build.ini"

    config = configparser.ConfigParser()
    config.read(cw_version_ini)

    version_info = {}
    for k,v in config["INFO"].items():
        version_info[k] = v

    return version_info

