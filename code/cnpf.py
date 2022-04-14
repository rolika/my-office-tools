import pathlib
import shutil
import configparser


def create_new_project_folder(**kwargs):
    """Create a new project folder"""
    # TODO: without arguments, the function should look for a configuration file in the current folder
    # TODO: with arguments src and dst, the function should create a new project folder in dst using the folder src
    # TODO: the function should return the path of the new project folder
    # TODO: with argument name, the function should rename the newly created project folder to name
    name = kwargs.pop("name", "new_project")
    src = kwargs.pop("src", "")
    dst = kwargs.pop("dst", "")
    src = pathlib.Path(src)
    dst = pathlib.Path(dst)
    # Create a new project folder
    project_folder = dst.joinpath(name)
    # Check if the folder already exists
    if project_folder.exists():
        # If the folder already exists, delete it
        shutil.rmtree(str(project_folder))
    # Create the new folder
    project_folder.mkdir()
    return project_folder


if __name__ == "__main__":
    pass