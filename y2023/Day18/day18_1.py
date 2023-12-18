import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import math
filepath = pathlib.Path(__file__).parent.resolve()
import copy

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    instructions = []
    for line in data:
        direction, length, RGBcode = line.split()
        instructions.append((direction, length))
    max_x, max_y = 0, 0
    min_y, min_x = math.inf, math.inf
    map_points = []
    current_x = 0
    current_y = 0
    for direction, length in instructions:
        for i in range(int(length)):
            if direction == "L":
                dx, dy = -1, 0
            elif direction == "R":
                dx, dy = 1, 0
            elif direction == "U":
                dx, dy = 0, -1
            elif direction == "D":
                dx, dy = 0, 1
            current_x += dx
            current_y += dy
            map_points.append((current_x, current_y))
            min_x = min_x if min_x < current_x else current_x
            min_y = min_y if min_y < current_y else current_y
            max_x = max_x if max_x > current_x else current_x
            max_y = max_y if max_y > current_y else current_y

    mapping = [[","]*(max_x-min_x+1) for _ in range(min_y, max_y+1)]
    for point in map_points:
        mapping[point[1]-min_y][point[0]-min_x] = "#"
    for line in mapping:
        print("".join(line))

    print()
    inside_point = (2, 25)
    next_points = [inside_point]
    while next_points:
        this_point = next_points.pop()
        if mapping[this_point[1]][this_point[0]] == "#":
            continue
        else:
            mapping[this_point[1]][this_point[0]] = "#"
        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0,-1)):
            new_x = this_point[0]+dx
            new_y = this_point[1]+dy
            if 0<new_x<(max_x-min_x) and 0<new_y<(max_y-min_y):
                next_points.append((new_x, new_y))
    total = 0
    for line in mapping:
        total += line.count("#")

    return total


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
