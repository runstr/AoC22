import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def flip_north(data):
    new_data = [["."]*len(data[0]) for i in data]
    for x in range(len(data[0])):
        next_y = 0
        for y in range(len(data)):
            if data[y][x] == "O":
                new_data[next_y][x] = "O"
                next_y += 1
            elif data[y][x] == "#":
                new_data[y][x] = "#"
                next_y = y+1
    return new_data


def flip_east(data):
    new_data = [["."]*len(data[0]) for i in data]
    for y in range(len(data)):
        next_x = len(data[0])-1
        for x in range(len(data[0])-1, -1, -1):
            if data[y][x] == "O":
                new_data[y][next_x] = "O"
                next_x -= 1
            elif data[y][x] == "#":
                new_data[y][x] = "#"
                next_x = x-1
    return new_data

def flip_south(data):
    new_data = [["."]*len(data[0]) for i in data]
    for x in range(len(data[0])):
        next_y = len(data)-1
        for y in range(len(data)-1, -1, -1):
            if data[y][x] == "O":
                new_data[next_y][x] = "O"
                next_y -= 1
            elif data[y][x] == "#":
                new_data[y][x] = "#"
                next_y = y-1
    return new_data

def flip_west(data):
    new_data = [["."]*len(data[0]) for i in data]
    for y in range(len(data)):
        next_x = 0
        for x in range(len(data[0])):
            if data[y][x] == "O":
                new_data[y][next_x] = "O"
                next_x += 1
            elif data[y][x] == "#":
                new_data[y][x] = "#"
                next_x = x+1
    return new_data


def calculate_load(data):
    j = len(data)
    total_load = 0
    for line in data:
        total_load += line.count("O")*j
        j -= 1
    return total_load


def get_my_answer():
    data = load_data_as_lines(filepath, example=True)
    total_loads = {}
    i = 1
    loops = 0
    loop_start = False
    while i <= 1000:
        data = flip_north(data)
        data = flip_west(data)
        data = flip_south(data)
        data = flip_east(data)
        total_load = calculate_load(data)
        if total_load in total_loads:
            if loop_start:
                loops += 1
            else:
                loop_start = True
            total_loads[total_load].append(i)
        else:
            total_loads[total_load] = [i]
            loop_start = False
            loop_start = 0
        if loops > 100:
            break
        i += 1
    loops = []
    for key, value in total_loads.items():
        if len(value) > 1:
            loops.append(value[-1]-value[-2])
    print(loops)

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
