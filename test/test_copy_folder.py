import pytest
import pathlib
import shutil
from code import create_new_project_folder


class TestCopyFolder:

    def setup_method(self):
        self._fromfolder = pathlib.Path(__file__).parent.absolute()
        self._tofolder = pathlib.Path(__file__).parent.absolute()

    def test_copy_folder(self):
        """Test the copy mechanism of an existing sample folder"""
        # Create a new project folder
        project_folder = create_new_project_folder(self._fromfolder, self._tofolder)
        # Copy the sample folder
        shutil.copytree(
            str(pathlib.Path(__file__).parent.absolute()) + "/sample_folder",
            str(project_folder) + "/sample_folder")
        # Check if the folder was copied
        assert project_folder.exists()
        assert project_folder.is_dir()
        # Check if the files were copied
        assert project_folder.joinpath("sample_folder").exists()
        assert project_folder.joinpath("sample_folder").is_dir()
        assert project_folder.joinpath("sample_folder").joinpath("file1.txt").exists()
        assert project_folder.joinpath("sample_folder").joinpath("file1.txt").is_file()
        assert project_folder.joinpath("sample_folder").joinpath("file2.txt").exists()
        assert project_folder.joinpath("sample_folder").joinpath("file2.txt").is_file()
        assert project_folder.joinpath("sample_folder").joinpath("file3.txt").exists()
        assert project_folder.joinpath("sample_folder").joinpath("file3.txt").is_file()
        assert project_folder.joinpath("sample_folder").joinpath("file4.txt").exists()
        assert project_folder.joinpath("sample_folder").joinpath("file4.txt").is_file()
        assert project_folder.joinpath("sample_folder").joinpath("file5.txt").exists()
        assert project_folder.joinpath("sample_folder").joinpath("file5.txt").is_file()
        assert project_folder.joinpath("sample_folder").joinpath("file6.txt").exists()
        assert project_folder.joinpath("sample_folder").joinpath("file6.txt").is_file()
    
    def teardown_method(self):
        pass