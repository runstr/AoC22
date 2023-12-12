import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def verify_next_possible(my_map, count, conditions, possible_combinations):
    if my_map == "":
        if not possible_combinations:
            possible_combinations[0] += 1
        return

    if count > conditions[0]:
        return
    if not conditions:
        return
    if my_map[0] == "." and count > 0:
        if conditions[0] != count:
            return
        conditions = []
        count = 0

    if my_map[0] == "?":
        verify_next_possible(my_map[1:], count+1, conditions, possible_combinations)
        verify_next_possible(my_map[1:], 0, conditions, possible_combinations)
    elif my_map[0] == "#":
        verify_next_possible(my_map[1:], count+1, conditions, possible_combinations)
    else:
        verify_next_possible(my_map[1:], 0, conditions, possible_combinations)

def get_my_answer():
    data = load_data_as_lines(filepath, example=True)
    total_combinations = []
    new_data = []
    for line in data:
        my_map, conditions = line.split(" ")
        mymap = (my_map+"?")
        conditions = (conditions+",")
        new_data.append((mymap[:-1], conditions[:-1]))

    for my_map, conditions in new_data:
        possible_combinations = [0]
        conditions = list(map(int, conditions.split(",")))
        count = 0
        if my_map[0] == "?":
            verify_next_possible(my_map[1:], count + 1, conditions, possible_combinations)
            verify_next_possible(my_map[1:], 0, conditions, possible_combinations)
        elif my_map[0] == "#":
            verify_next_possible(my_map[1:], count + 1, conditions, possible_combinations)
        else:
            verify_next_possible(my_map[1:], 0, conditions, possible_combinations)
        total_combinations.append(possible_combinations)
    return sum(total_combinations)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
