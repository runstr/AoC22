import pathlib
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
            else:
                raise Exception("WRONG")
        new_rule.append(all_rules[-1])
        new_rules[letters] = new_rule
    return new_rules

def check_rules(part, rules):
    for rule in rules[:-1]:
        part_value = part[rule[0]]
        rule_value = rule[1]
        if rule_value < 0 and rule_value+part_value < 0:
            return rule[2]
        elif rule_value > 0 < part_value > rule_value:
            return rule[2]
    return rules[-1]

def transform_parts(parts):
    new_parts = []
    for part in parts:
        new_part = {}
        for p in part[1: -1].split(","):
            letter, value = p.split("=")
            new_part[letter] = int(value)
        new_parts.append(new_part)
    return new_parts

def get_my_answer():
    rules, parts = load_data(filepath, example=False).split("\n\n")
    rules = transform_rules(rules.split("\n"))
    parts = transform_parts(parts.split("\n"))
    accepted_parts = []
    for part in parts:
        destination = "in"
        while True:
            rule = rules[destination]
            destination = check_rules(part, rule)
            if destination == "A":
                accepted_parts.append(part)
                break
            elif destination == "R":
                break




    print(rules)
    print(parts)


    return sum([sum(part.values()) for part in accepted_parts])


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
