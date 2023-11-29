import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def perform_operation(old, operation, value):
    if not value.isdigit():
        value = old
    if operation == "*":
        return old*int(value)
    elif operation == "+":
        return old+int(value)


def get_my_answer():
    data = load_data(filepath, example=False)
    monkeys = data.split("\n\n")
    monkey_items, monkey_operations, monkey_test, monkey_true, monkey_false = [], [], [], [], []
    monkey_inspections = [0 for i in range(0, len(monkeys))]
    #Decode monkey operations
    for monkey in monkeys:
        lines = monkey.split(("\n"))
        monkey_items.append(list(map(int, lines[1].split(": ")[1].split(", "))))
        monkey_operations.append(lines[2].split(": ")[1].split(" = ")[1].split())
        monkey_test.append(int(lines[3].split()[-1]))
        monkey_true.append(int(lines[4].split()[-1]))
        monkey_false.append(int(lines[5].split()[-1]))
    for round in range(0, 20):
        for monkey in range(0, len(monkey_items)):
            for i, monkey_item in enumerate(monkey_items[monkey]):
                monkey_inspections[monkey] += 1
                new = perform_operation(monkey_item, monkey_operations[monkey][1], monkey_operations[monkey][2])//3
                if new % monkey_test[monkey] == 0:
                    monkey_items[monkey_true[monkey]].append(new)
                else:
                    monkey_items[monkey_false[monkey]].append(new)
            monkey_items[monkey] = []
    monkey_inspections.sort()
    return monkey_inspections[-1]*monkey_inspections[-2]


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
