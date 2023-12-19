import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
POSSIBLE_COMBO = 0


def verify_next_possible(index, my_map, remaining_conditions, checked_maps):
    key = (my_map[index:], tuple(remaining_conditions))
    if key in checked_maps:
        return checked_maps[key]
    if remaining_conditions == []:
        if "#" not in my_map[index:]:
            checked_maps[key] = 1
            return 1
        checked_maps[key] = 0
        return 0

    if my_map[index:].count("#")+my_map[index:].count("?") < sum(remaining_conditions):
        checked_maps[key] = 0
        return 0
    if my_map[index] == "#":
        if "." in my_map[index:index+remaining_conditions[0]]:
            checked_maps[key] = 0
            return 0
        if len(my_map[index:]) > remaining_conditions[0]:
            if my_map[index+remaining_conditions[0]] == "#":
                checked_maps[key] = 0
                return 0
        new_index = index + remaining_conditions[0] + 1
        old_map = my_map[:index]
        middle_map = "#"*remaining_conditions[0]+"."
        rest_map = my_map[new_index:]
        return verify_next_possible(new_index, old_map+middle_map+rest_map, remaining_conditions[1:], checked_maps)
    elif my_map[index] == ".":
        return verify_next_possible(index+1, my_map, remaining_conditions, checked_maps)
    else:
        total = (verify_next_possible(index, my_map[:index]+"."+my_map[index+1:], remaining_conditions, checked_maps) +
        verify_next_possible(index, my_map[:index]+"#"+my_map[index+1:], remaining_conditions, checked_maps))
        checked_maps[key] = total
        return total

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    new_data = []
    for line in data:
        my_map, conditions = line.split(" ")
        mymap = (my_map+"?")*5
        conditions = (conditions+",")*5
        new_data.append((mymap[:-1], conditions[:-1]))
    all_values = []
    for my_map, conditions in new_data:
        checked_maps = {}
        conditions = list(map(int, conditions.split(",")))
        total = verify_next_possible(0, my_map, conditions, checked_maps)
        print(total)
        all_values.append(total)
    return sum(all_values)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
