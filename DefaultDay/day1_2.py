import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int

filepath = pathlib.Path(__file__).parent.resolve()


def execution():
    print(load_data(filepath, True))