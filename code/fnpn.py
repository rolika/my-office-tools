"""
The projects are listed in a LibreOffice Calc spreadsheet, in multiple sheets which are named after the current
year, like 2022. Sheets have some header rows, mostly 7, so projects start in row 8.
But this can be changed anytime, so the function has to look up for the project number pattern:
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


DEFAULT_CONFIG_FILE = "data/config.ini"
SOFFICE_COMMAND_LINE = """soffice --accept="pipe,name=wrk;urp;" --norestore --nologo --nodefault --headless"""


def fetch_next_project_number(**kwargs) -> str:
    """Fetch the next available project number from the projects spreadsheet.
    Needs a config.ini file ind the data folder, which contains the path to the projectsheet.

    Known keywords - provided by the caller with values as strings:
        cfg:    config file
        sht:    path to the projectsheet - providing it will override the config file
    
    Raises:     FileNotFoundError if the config file or the project sheet is not found
    
    Returns:    project number in yy/nnn format as a string"""

    # saddle the workhorse
    sub = subprocess.Popen(shlex.split(SOFFICE_COMMAND_LINE))
    session = pyoo.Desktop(pipe="wrk")
    
    # parse the config file - default values
    cfg = kwargs.pop("cfg", DEFAULT_CONFIG_FILE)
    config = configparser.ConfigParser()
    config.read(cfg)  # this is empty if the config file does not exist
    cfg_sht = config.get("path", "sht", fallback=None)

    # parse the kwargs and overwrite default values if necessary
    sht = kwargs.pop("sht", cfg_sht)

    sht = pathlib.Path(sht)

    if sht.exists() and sht.is_file():
        # open the project sheet
        doc = session.open_spreadsheet(sht)
        doc.close()
    else:
        raise FileNotFoundError(f"File not found: {sht}")


if __name__ == "__main__":
    print(fetch_next_project_number())