import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    total_load = {i: [] for i in range(len(data[0]))}
    for x in range(len(data[0])):
        next_load = len(data)
        for y in range(len(data[0])):
            if data[y][x] == "O":
                total_load[x].append(next_load)
                next_load-=1
            elif data[y][x] == "#":
                next_load = len(data)-y-1
    print(total_load)
    total_sum = 0
    for value in total_load.values():
        total_sum+=sum(value)
    return total_sum

def temp(data):
    rocks = {}
    square_rocks = {}
    for y, line in enumerate(data):
        next_i = 0
        for x, rock in enumerate(line):
            if rock == "O":
                rocks[x].append(y)
            elif rock == "#":
                square_rocks[x].append(y)
    new_rocks = {i: [] for i in range(len(data[0]))}

@timeexecution
def execution():
    submit_answer = True
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
