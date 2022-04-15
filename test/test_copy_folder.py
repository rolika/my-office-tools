import shutil
import unittest
import pathlib
from code import cnpf


class TestCopyFolder(unittest.TestCase):

    def test_copy_folder(self):
        """Test the copy mechanism of an existing sample folder"""
        self._project_folder = cnpf.create_new_project_folder(src="test/sampleproject", dst="test/projects")
        self.assertTrue(pathlib.Path("test", "projects", "sampleproject").exists(), "Folder not copied")

    def test_copy_folder_rename(self):
        """Test the copy mechanism of an existing sample folder, but with a different name"""
        self._project_folder = cnpf.create_new_project_folder(src="test/sampleproject", dst="test/projects", name="new_project")
        self.assertTrue(pathlib.Path("test", "projects", "new_project").exists(), "Renamed folder not copied")

    def test_copy_folder_config(self):
        """Test the copy mechanism of an existing sample folder with location specified in an ini file."""
        self._project_folder = cnpf.create_new_project_folder(cfg="test/config.ini")
        self.assertTrue(pathlib.Path("test", "projects", "new_project").exists(), "Folder not copied")

    def test_copy_folder_config_default(self):
        """Test the copy mechanism with a default config file.
        The default config file must be located in the data folder and named as config.ini"""
        self._project_folder = cnpf.create_new_project_folder()
        self.assertTrue(pathlib.Path("test", "projects", "sampleproject").exists(), "Folder not copied")

    def tearDown(self):
        shutil.rmtree(self._project_folder)