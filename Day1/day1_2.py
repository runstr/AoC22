import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_most_calories():
    data = load_data_as_lines(filepath, example=False)
    max_calories_1 = 0
    max_calories_2 = 0
    max_calories_3 = 0
    total_calories = 0
    for line in data:
        if line == "":
            if total_calories >= max_calories_1:
                max_calories_3 = max_calories_2
                max_calories_2 = max_calories_1
                max_calories_1 = total_calories
            elif total_calories >= max_calories_2:
                max_calories_3 = max_calories_2
                max_calories_2 = total_calories
            elif total_calories >= max_calories_3:
                max_calories_3 = total_calories
            total_calories = 0
        else:
            total_calories += int(line)
    if total_calories >= max_calories_1:
        max_calories_3 = max_calories_2
        max_calories_2 = max_calories_1
        max_calories_1 = total_calories
    elif total_calories >= max_calories_2:
        max_calories_3 = max_calories_2
        max_calories_2 = total_calories
    elif total_calories >= max_calories_3:
        max_calories_3 = total_calories
    return max_calories_1+max_calories_2+max_calories_3


@timeexecution
def execution():
    answer = get_most_calories()
    #submit(answer, part="b", day=1, year=2022)
