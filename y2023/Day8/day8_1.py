import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()



def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    instructions = data[0]
    maps = {}
    for line in data[2:]:
        start, end = line.split(" = ")
        left, right = end[1:-1].split(", ")
        maps[start] = [left, right]
    i = 0
    instructions_length = len(instructions)
    next_map = "AAA"
    while next_map != "ZZZ":
        instruction = instructions[i % instructions_length]
        if instruction == "L":
            next_map = maps[next_map][0]
        else:
            next_map = maps[next_map][1]
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
