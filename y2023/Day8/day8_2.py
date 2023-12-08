import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def verify_nodes(nodes):
    for node in nodes:
        if node[2] != "Z":
            return False
    return True

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    instructions = data[0]
    maps = {}
    next_nodes = []
    for line in data[2:]:
        start, end = line.split(" = ")
        left, right = end[1:-1].split(", ")
        maps[start] = [left, right]
        if start[2] == "A":
            next_nodes.append(start)
    i = 0
    instructions_length = len(instructions)
    while not verify_nodes(next_nodes):
        instruction = instructions[i % instructions_length]
        new_next_nodes = []
        if instruction == "L":
            for node in next_nodes:
                new_next_nodes.append(maps[node][0])
        else:
            for node in next_nodes:
                new_next_nodes.append(maps[node][1])
        next_nodes = new_next_nodes
        i += 1
    return i


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
