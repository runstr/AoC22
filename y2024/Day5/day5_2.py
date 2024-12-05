import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
global ruleset
def get_rules_and_orders(data):
    rules = []
    orders = []
    set_rules = True
    for line in data:
        if line == "":
            set_rules= False
            continue
        if set_rules:
            rules.append(line)
        else:
            orders.append(line)
    return rules, orders

def get_my_answer():
    data = load_data_as_lines(filepath, example=True)
    rules, orders = get_rules_and_orders(data)
    ruleset = {}
    for rule in rules:
        first, second = tuple(map(int,rule.split("|")))
        try:
            ruleset[first].append(second)
        except:
            ruleset[first] = [second]
    correct_orders = []
    for order in orders:
        order = list(map(int, order.split(",")))
        print(order)
        correct = sorting_rule(order)
        if correct:
            correct_orders.append(order)
    print(correct_orders)
    total_sum = 0
    for order in correct_orders:
        total_sum+=order[len(order)//2]
    print(ruleset)
    return total_sum

def sorting_rule(order):
    correct = True
    for i in range(len(order) - 1, -1, -1):
        first_part = order[:i]
        print(first_part)
        try:
            rules = ruleset[order[i]]
            for rule in rules:
                if rule in first_part:
                    correct = False
                    break
        except:
            pass
        if not correct:
            return False
    return True

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
