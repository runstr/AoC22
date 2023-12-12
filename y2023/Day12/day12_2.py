import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def verify_next_possible(my_map, conditions, possible_combinations, new_map):
    if my_map.count("#")+my_map.count("?") < sum(conditions):
        return
    if my_map[0] == ".":
        verify_next_possible(my_map[1:], conditions, possible_combinations, new_map + ".")

    if new_map[-1] == "#":
        if len(my_map) < conditions[0]-1:
            return
        if "." in my_map[:conditions[0]-1]:
            return
        if len(my_map) == conditions[0]-1:
            possible_combinations.append(new_map+"#"*(conditions[0]-1))
            return
        if my_map[conditions[0]] == "#":
            return
        if len(conditions) == 1:
            possible_combinations.append(new_map+"#"*(conditions[0]-1)+my_map[conditions[0]:])
            return
        verify_next_possible(my_map[conditions[0]:], conditions[1:], possible_combinations, new_map+"#"*(conditions[0]-1) + ".")

    if my_map[0] == "#":
        verify_next_possible(my_map[1:], conditions, possible_combinations, new_map + "#")
    elif my_map[0] == "?":
        verify_next_possible(my_map[1:], conditions, possible_combinations, new_map + ".")
        verify_next_possible(my_map[1:], conditions, possible_combinations, new_map + "#")

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
        my_map
        possible_combinations = []
        conditions = list(map(int, conditions.split(",")))
        new_map = ""
        if my_map[0] == "?":
            verify_next_possible(my_map[1:], conditions, possible_combinations, new_map+"#")
            verify_next_possible(my_map[1:], conditions, possible_combinations, new_map+".")
        elif my_map[0] == "#":
            verify_next_possible(my_map[1:], conditions, possible_combinations, new_map+"#")
        else:
            verify_next_possible(my_map[1:], conditions, possible_combinations, new_map+".")
        #print(possible_combinations)
        total_combinations.append(len(possible_combinations))
    return sum(total_combinations)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
