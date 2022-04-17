import pathlib
import shutil
import unittest
from code import cnpf


class TestCreateFolder(unittest.TestCase):
    """Test creating a project folder specified in a json file."""

    def test_create_folder(self):
        """Test creating a project folder."""
        self._project_folder = cnpf.create_new_project_folder(crt="data/create.txt")
        self.assertTrue(pathlib.Path("test", "projects", "sampleproject").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "sampleproject", "test").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "sampleproject", "code", "sample", "simple.py").exists(), "File not copied")
        self.assertTrue(pathlib.Path("test", "projects", "sampleproject", "README.md").exists(), "File not copied")

    def test_create_folder_with_name(self):
        """Test creating a project folder."""
        self._project_folder = cnpf.create_new_project_folder(crt="data/create.txt", name="my_newest_project")
        self.assertTrue(pathlib.Path("test", "projects", "my_newest_project").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "my_newest_project", "test").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "my_newest_project", "code", "sample", "simple.py").exists(), "File not copied")
        self.assertTrue(pathlib.Path("test", "projects", "my_newest_project", "README.md").exists(), "File not copied")

    def test_create_folder_default_with_name(self):
        """Test creating a project folder."""
        self._project_folder = cnpf.create_new_project_folder(name="my_shiny_new_project")
        self.assertTrue(pathlib.Path("test", "projects", "my_shiny_new_project").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "my_shiny_new_project", "test").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "my_shiny_new_project", "code", "sample", "simple.py").exists(), "File not copied")
        self.assertTrue(pathlib.Path("test", "projects", "my_shiny_new_project", "README.md").exists(), "File not copied")

    def tearDown(self):
        shutil.rmtree(self._project_folder)
