import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def divide_into_groups():
    groups = []
    data = load_data_as_lines(filepath, example=False)
    new_group = []
    for i, line in enumerate(data):
        if (i+1) % 3 == 0:
            new_group.append(line)
            groups.append(new_group)
            new_group = []
        else:
            new_group.append(line)
    return groups


def get_my_answer():
    groups = divide_into_groups()
    total_priority = 0
    for group in groups:
        same_value = (set(group[0]) & set(group[1]) & set(group[2])).pop()
        if same_value.isupper():
            total_priority += (ord(same_value) - 38)
        else:
            total_priority += (ord(same_value) - 96)
    return total_priority


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
