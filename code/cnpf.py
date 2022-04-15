import pathlib
import shutil
import configparser


def create_new_project_folder(**kwargs):
    """Create a new project folder"""
    src = kwargs.pop("src", "")
    dst = kwargs.pop("dst", "")
    src = pathlib.Path(src)
    name = kwargs.pop("name", src.name)
    dst = pathlib.Path(dst).joinpath(name)
    project_folder = shutil.copytree(src, dst, dirs_exist_ok=True)
    return project_folder


if __name__ == "__main__":
    pass