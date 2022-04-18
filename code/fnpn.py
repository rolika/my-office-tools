"""
The projects are listed in a LibreOffice Calc spreadsheet, in multiple sheets which are named after the current
year, like 2022. Sheets have some header rows, mostly 7, so projects start in row 8.
But this can be changed anytime, so the function has to look up for the  first project number pattern in column A:
Project numbers are in the A-column, start with two-digit years, separated with a slash '/', followed by the
actual project number starting with 1: yy/n or yy/nn or yy/nnn.
Project numbers are predefined in column A, mostly at least until 500, but it cannot be assumed for sure.
Not taken project numbers have an empty cell in column B next to them.
"""


import subprocess
import shlex
import configparser
import pathlib
import pyoo
import datetime
import re


DEFAULT_CONFIG_FILE = "data/config.ini"
SOFFICE_COMMAND_LINE = """soffice --accept="pipe,name=wrk;urp;" --norestore --nologo --nodefault --headless"""
RE_PROJECT_NUMBER = re.compile(r"^\d{2}/\d{1,3}$")  # yy/n or yy/nn or yy/nnn


def fetch_next_project_number(**kwargs) -> str:
    """Fetch the next available project number from the projects spreadsheet.
    Needs a config.ini file ind the data folder, which contains the path to the projectsheet.

    Known keywords - provided by the caller with values as strings:
        cfg:    config file
        sht:    path to the projectsheet - providing it will override the config file
        year:   year 'yyyy' - providing it will override the use of the current year

    Raises:     FileNotFoundError if the the project sheet is not found

    Returns:    project number in yy/nnn format as a string"""

    # saddle the workhorse
    subprocess.run(shlex.split(SOFFICE_COMMAND_LINE))
    session = pyoo.Desktop(pipe="wrk")

    # parse the config file - default values
    cfg = kwargs.pop("cfg", DEFAULT_CONFIG_FILE)
    config = configparser.ConfigParser()
    config.read(cfg)  # this is empty if the config file does not exist
    cfg_sht = config.get("path", "sht", fallback=None)
    projectnum_col = config.getint("path", "projectnum_col", fallback=0)
    project_col = config.getint("path", "project_col", fallback=1)
    start_row = config.getint("path", "start_row", fallback=7)

    # get current calendar year
    current_year = str(datetime.datetime.now().year)  # should be a string

    # parse the kwargs and overwrite default values if necessary
    sht = kwargs.pop("sht", cfg_sht)
    year = kwargs.pop("year", current_year)
    year = year[:4]  # only the first four digits are used

    sht = pathlib.Path(sht)

    if sht.exists() and sht.is_file():
        doc = session.open_spreadsheet(sht)

        # make sure the sheet exists
        try:
            sheet = doc.sheets[year]
        except KeyError:
            doc.close()
            raise ValueError(f"sheet not found: {year}")

        # sheet ok, find the next empty project cell
        row = _find_next_empty_cell(sheet, start_row, project_col)
        mo = RE_PROJECT_NUMBER.search(sheet[row, projectnum_col].value)
        if mo:  # there is valid project number in the cell
            doc.close()
            return mo.group()
    else:
        raise FileNotFoundError(f"file not found: {sht}")


def _find_next_empty_cell(sheet:pyoo.Sheet, row:int, col:int) -> tuple:
    """Find the next empty cell in the column.
    The cell is returned as a tuple (row, column)

    Args:       sheet:  the sheet to search in
                row:    the row to start searching from
                col:    the column to search in

    Returns:    row"""

    while True:
        if sheet[row, col].value == "":
            return row
        row += 1


if __name__ == "__main__":
    print(fetch_next_project_number())