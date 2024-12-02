import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    all_data = load_data_as_lines(filepath, example=False)
    first_list, second_list = [], []
    for line in all_data:
        new_line = line.split("   ")
        first_list.append(int(new_line[0]))
        second_list.append(int(new_line[1]))
    first_list.sort()
    second_list.sort()
    difference = 0
    for i in range(len(first_list)):
        difference+=abs(second_list[i]-first_list[i])
    print(difference)


get_my_answer()