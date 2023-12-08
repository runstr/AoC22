import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    instructions = data[0]
    node_map = {}
    for line in data[2:]:
        start, end = line.split(" = ")
        node_map[start] = [*end[1:-1].split(", ")]
    i = 0
    instructions_length = len(instructions)
    next_node = "AAA"
    while next_node != "ZZZ":
        instruction = instructions[i % instructions_length]
        next_node = node_map[next_node][0] if instruction == "L" else node_map[next_node][1]
        i += 1
    return i


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
