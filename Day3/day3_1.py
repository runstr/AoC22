import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    total_priority = 0
    for line in data:
        first = set(line[:int(len(line)/2)])
        second = set(line[int(len(line)/2):])
        common_letter = (first & second).pop()
        if common_letter.isupper():
            total_priority += (ord(common_letter) - 38)
        else:
            total_priority += (ord(common_letter) - 96)
    return total_priority


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
