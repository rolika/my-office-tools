import pathlib
import shutil
import configparser


def create_new_project_folder(**kwargs):
    """Create a new project folder"""
    src = kwargs.pop("src", None)
    dst = kwargs.pop("dst", None)

    if not src:
        raise ValueError("src is required")
    if not dst:
        raise ValueError("dst is required")

    src = pathlib.Path(src)

    if src.exists() and src.is_dir():
        name = kwargs.pop("name", src.name)

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