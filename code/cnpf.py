import pathlib
import shutil
import configparser
import tempfile
import argparse


DEFAULT_CONFIG_FILE = "data/config.ini"


def create_new_project_folder(**kwargs):
    """Create a new project folder.
    Calling without arguments the default config file in the data folder is used.
    Specifying source, destination and name will override the config file.
    Known keywords - provided by the caller with values as strings:
        src:    source folder
        dst:    destination folder
        name:   name of the new project folder
        cfg:    config file
        crt:    txt file holding the folder structure to be created
    The create.txt is layed out as follows:
        - names before a colon (:) are treated as folder names
        - names after a colon (:) are treated as file names, separated by spaces
        A colon with no name before it is treated as the root folder.
    If the config file contains a reference to a folder create structure, it is used by default.
    """

    # parse the config file - default values
    cfg = kwargs.pop("cfg", DEFAULT_CONFIG_FILE)
    config = configparser.ConfigParser()
    config.read(cfg)  # this is empty if the config file does not exist
    cfg_src = config.get("path", "src", fallback=None)
    cfg_dst = config.get("path", "dst", fallback=None)
    cfg_crt = config.get("path", "crt", fallback=None)

    # parse the kwargs and overwrite default values if necessary
    src = kwargs.pop("src", cfg_src)
    dst = kwargs.pop("dst", cfg_dst)
    crt = kwargs.pop("crt", cfg_crt)

    # parse the create file if present and overwrite previous values if necessary
    if crt:
        try:
            with open(crt, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {crt}")

        # create a temporary folder to leave the rest of the code logic unchanged
        tmpdir = tempfile.mkdtemp()
        for line in lines:
            folder, files = line.split(":", 1)
            folder = pathlib.Path(tmpdir, folder.strip())
            folder.mkdir(parents=True, exist_ok=True)
            for file in files.split():
                file = pathlib.Path(file.strip())
                if file.is_file():
                    shutil.copyfile(file, folder / file.name)
                else:
                    raise FileNotFoundError(f"File not found: {file}")                
        src = tmpdir

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
            raise ValueError("destination folder already exists")

        shutil.copytree(src, dst)
        return dst

    else:
        raise ValueError("source folder does not exist or is not a directory")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new project folder.")
    parser.add_argument("--src", help="source folder")
    parser.add_argument("--dst", help="destination folder")
    parser.add_argument("--name", help="name of the new project folder")
    parser.add_argument("--cfg", help="config file")
    parser.add_argument("--crt", help="folder create file")
    args = {k: v for k, v in vars(parser.parse_args()).items() if v}
    create_new_project_folder(**args)