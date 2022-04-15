import pathlib
import shutil
import unittest
from code import cnpf


class TestCreateFolder(unittest.TestCase):
    """Test creating a project folder specified in a json file."""

    def test_create_folder(self):
        """Test creating a project folder."""
        self._project_folder = cnpf.create_new_project_folder(jsn="data/project_folder.json")
        self.assertTrue(pathlib.Path("test", "projects", "new_project").exists(), "Folder not copied")

    def tearDown(self):
        shutil.rmtree(self._project_folder)
