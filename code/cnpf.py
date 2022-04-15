import pathlib
import shutil
import configparser
import json


DEFAULT_CONFIG_FILE = "data/config.ini"


def create_new_project_folder(**kwargs):
    """Create a new project folder.
    Calling without arguments the default config file in the data folder is used.
    Specifying source, destination and name will override the config file.
    Specifying a json file, a destination folder must be specified as well.
    Known keywords - provided by the caller with values as strings:
        src:    source folder
        dst:    destination folder
        name:   name of the new project folder
        cfg:    config file
        jsn:    json file
    """

    # parse the config file - default values
    cfg = kwargs.pop("cfg", DEFAULT_CONFIG_FILE)
    config = configparser.ConfigParser()
    config.read(cfg)  # this is empty if the config file does not exist
    cfg_src = config.get("path", "src", fallback=None)
    cfg_dst = config.get("path", "dst", fallback=None)

    # parse the kwargs and overwrite default values if necessary
    src = kwargs.pop("src", cfg_src)
    dst = kwargs.pop("dst", cfg_dst)

    if not src:
        raise ValueError("source folder is required")
    if not dst:
        raise ValueError("destination folder is required")

    src = pathlib.Path(src)

    if src.exists() and src.is_dir():
        cfg_name = config.get("path", "name", fallback=src.name)
        name = kwargs.pop("name", cfg_name)

        dst = pathlib.Path(dst)
        if dst.exists() and dst.is_dir():
            dst = dst / name
        if dst.exists():
            raise ValueError("target folder already exists")

        shutil.copytree(src, dst)
        return dst

    else:
        raise ValueError("source folder does not exist or is not a directory")


if __name__ == "__main__":
    pass