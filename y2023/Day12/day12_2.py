import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
from cachetools import cached, LRUCache, TTLCache
POSSIBLE_COMBO = 0

DP = {}
def verify_next_possible(index, my_map, remaining_conditions):
    global POSSIBLE_COMBO
    key = (my_map[:index], tuple(remaining_conditions))
    if key in DP:
        return DP[key]
    if remaining_conditions == []:
        DP[key] = 1
        return 1

    if my_map[index:].count("#")+my_map[index:].count("?") < sum(remaining_conditions):
        return 0
    if my_map[index] == "#":
        if "." in my_map[index:index+remaining_conditions[0]]:
            return 0
        if len(my_map[index:]) > remaining_conditions[0]:
            if my_map[index+remaining_conditions[0]] == "#":
                return 0
        new_index = index + remaining_conditions[0] + 1
        old_map = my_map[:index]
        middle_map = "#"*remaining_conditions[0]+"."
        rest_map = my_map[new_index:]
        return verify_next_possible(new_index, old_map+middle_map+rest_map, remaining_conditions[1:])
    elif my_map[index] == ".":
        return verify_next_possible(index+1, my_map, remaining_conditions)
    else:
        total = (verify_next_possible(index, my_map[:index]+"."+my_map[index+1:], remaining_conditions)+
                verify_next_possible(index, my_map[:index]+"#"+my_map[index+1:], remaining_conditions))
        DP[key]=total
        return total

def get_my_answer():
    data = load_data_as_lines(filepath, example=True)
    total_combinations = []
    new_data = []
    for line in data:
        my_map, conditions = line.split(" ")
        mymap = (my_map+"?")*5
        conditions = (conditions+",")*5
        new_data.append((mymap[:-1], conditions[:-1]))
    for my_map, conditions in new_data:
        conditions = list(map(int, conditions.split(",")))
        total_combinations.append(verify_next_possible(0, my_map, conditions))
    return sum(total_combinations)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
