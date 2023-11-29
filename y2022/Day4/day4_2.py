import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    subsets = 0
    for line in data:
        first_pair, second_pair = line.split(",")
        first_range = set(range(int(first_pair.split("-")[0]), int(first_pair.split("-")[1]) + 1))
        second_range = set(range(int(second_pair.split("-")[0]), int(second_pair.split("-")[1]) + 1))
        subsets += int(not first_range.isdisjoint(second_range))
    return subsets


@timeexecution
def execution():
    submit_answer = True
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
