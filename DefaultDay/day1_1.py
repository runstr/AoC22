import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution

filepath = pathlib.Path(__file__).parent.resolve()


@timeexecution
def execution():
    print(load_data(filepath, example=True))
