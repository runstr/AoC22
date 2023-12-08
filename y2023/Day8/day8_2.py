import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
import math

def find_repeat(next_node, node_map, instructions, instructions_length):
    i = 0
    while True:
        instruction = instructions[i % instructions_length]
        next_node = node_map[next_node][0] if instruction == "L" else node_map[next_node][1]
        i += 1
        if next_node[2] == "Z":
            return i


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    instructions = data[0]
    node_map = {}
    start_nodes = []
    for line in data[2:]:
        start, end = line.split(" = ")
        node_map[start] = [*end[1:-1].split(", ")]
        if start[2] == "A":
            start_nodes.append(start)
    all_numbers = []
    for node in start_nodes:
        all_numbers.append(find_repeat(node, node_map, instructions, len(instructions)))
    return math.lcm(*all_numbers)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
