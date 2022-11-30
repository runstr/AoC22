import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


@timeexecution
def execution():
    print(load_data(filepath, example=False))
    # submit(my_answer, part="a", day=1, year=2022)