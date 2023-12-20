import pathlib
from copy import deepcopy

from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def transform_rules(rules):
    new_rules = {}
    for rule in rules:
        letters, rest = rule.split("{")
        new_rule = []
        all_rules = rest[:-1].split(",")
        for r in all_rules[:-1]:
            letter, destination = r.split(":")
            if letter[1] == "<":
                new_rule.append((letter[0], -int(letter[2:]), destination))
            elif letter[1] == ">":
                new_rule.append((letter[0], int(letter[2:]), destination))
        new_rule.append(all_rules[-1])
        new_rules[letters] = new_rule
    return new_rules

def check_rules(part_range, rules):
    new_part_ranges = []
    for rule in rules[:-1]:
        part_values = part_range[rule[0]]
        min_value = part_values[0]
        max_value = part_values[1]
        rule_value = rule[1]
        destination = rule[2]
        if abs(rule_value) in range(min_value, max_value):
            new_part_range = deepcopy(part_range)
            if rule_value < 0:
                new_end_value = abs(rule_value)-1
                part_range[rule[0]] = (abs(rule_value), max_value)
                new_range = (min_value, new_end_value)
                new_part_range[rule[0]] = new_range
                new_part_ranges.append((destination, new_part_range))
            else:
                new_start_value = rule_value+1
                part_range[rule[0]] = (min_value, rule_value)
                new_range = (new_start_value, max_value)
                new_part_range[rule[0]] = new_range
                new_part_ranges.append((destination, new_part_range))
    new_part_ranges.append((rules[-1], part_range))
    return new_part_ranges

def get_my_answer():
    rules, parts = load_data(filepath, example=False).split("\n\n")
    rules = transform_rules(rules.split("\n"))
    accepted_parts = []
    part_ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    destination = "in"
    queue = [(destination, part_ranges)]
    while queue:
        destination, part_ranges = queue.pop()
        new_queue = check_rules(part_ranges, rules[destination])
        for dest, part_range in new_queue:
            if dest == "A":
                accepted_parts.append(part_range)
            elif dest == "R":
                continue
            else:
                queue.append((dest, part_range))

    total_combinations = 0
    for part in accepted_parts:
        combinations = 1
        for key, values in part.items():
            combinations *= len(range(values[0], values[1]+1))
        total_combinations+=combinations
    print(total_combinations)
    return accepted_parts


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
