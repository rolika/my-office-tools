import unittest
from code import fnpn


class TestFetchProjectNumber(unittest.TestCase):
    """Test fetching the next project number from the projects spreadsheet."""

    def test_fetch_project_number(self):
        self.assertEqual(fnpn.fetch_next_project_number(sht="data/projects.ods"), "22/122")