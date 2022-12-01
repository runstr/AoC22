import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution, time
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_most_calories():
    data = load_data_as_lines(filepath, example=False)
    max_calories = 0
    total_calories = 0
    for line in data:
        if line == "":
            if total_calories>max_calories:
                max_calories=total_calories
            total_calories = 0
        else:
            total_calories += int(line)
    return max_calories


@timeexecution
def execution():
    print(get_most_calories())
    #submit(get_most_calories(), part="a", day=1, year=2022)
