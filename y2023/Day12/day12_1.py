import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import math
filepath = pathlib.Path(__file__).parent.resolve()
import itertools


def get_all_indexes(string):
    return [i for i, val in enumerate(string) if val == "?"]


def generate_new_map(map, indexes, combinations):
    for i, index in enumerate(indexes):
        new_letter = "#" if combinations[i] else "."
        map = map[:index]+new_letter+map[index+1:]
    return map

def check_map(map, requirements):
    req_index = 0
    start = False
    count = 0
    for i in map:
        if start and i == ".":
            if count != requirements[req_index]:
                return False
            else:
                count = 0
                req_index += 1
                start = False
        elif i == "#":
            start = True
            count += 1
    if start and count != requirements[-1]:
        return False
    return True


def check_map2(map, requirements):
    map = "."+map+"."
    for key, value in requirements.items():
        count = 0
        for i in range(0, len(map) - len(key)+1):
            check_value = map[i:i+len(key)]
            if check_value == key:
                count += 1
        if count != value:
            return False
    return True


def generate_combinations(x, y):
    values = [False, True]
    return [combo for combo in itertools.product(values, repeat=x) if sum(combo)==y]
    pass

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    total_total_combinations = []
    new_data = []
    for line in data:
        my_map, conditions = line.split(" ")
        mymap = (my_map+"?")
        conditions = (conditions+",")
        new_data.append((mymap[:-1], conditions[:-1]))
    for my_map, conditions in new_data:
        unknowns = my_map.count("?")
        knowns = my_map.count("#")
        old_conditions = list(map(int, conditions.split(",")))
        total = sum(old_conditions)
        unknown_indexes = get_all_indexes(my_map)
        conditions = generate_combinations(unknowns, total-knowns)
        total_combinations = 0
        for condition in conditions:
            new_map = generate_new_map(my_map, unknown_indexes, condition)
            if check_map(new_map, old_conditions):
                total_combinations += 1
        total_total_combinations.append(total_combinations)
    return sum(total_total_combinations)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
