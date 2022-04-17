import pathlib
import shutil
import unittest
import subprocess
from code import cnpf


class TestFolderCmdLine(unittest.TestCase):
    """Test creating a project folder using the command line."""

    def test_create_folder_from_cmdline(self):
        subprocess.run(["python3", "code/cnpf.py", "--name", "my_newest_project"])
        self.assertTrue(pathlib.Path("test", "projects", "my_newest_project").exists(), "Folder not created")
        self.assertTrue(pathlib.Path("test", "projects", "my_newest_project", "README.md").exists(), "File not copied")

    def tearDown(self):
        shutil.rmtree(pathlib.Path("test", "projects", "my_newest_project"))