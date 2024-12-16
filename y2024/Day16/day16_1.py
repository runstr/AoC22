import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    cave_map ={}
    start_point = ()
    for y in range(len(data)):
        for x in range(len(data[0])):
            cave_map[(x,y)] = data[y][x]
            if data[y][x] == "S":
                start_point = (x, y)
    visited = dict()
    next_paths = [(start_point, (1, 0), 0, 0)]
    minimum_score = math.inf
    while next_paths:
        path, direction, turns, moves = next_paths.pop(0)
        total_score = turns*1000 + moves
        if total_score > minimum_score:
            continue
        if cave_map[path] == "E":
            if total_score < minimum_score:
                minimum_score = total_score
            continue
        if (path, direction) in visited:
            if total_score > visited[(path, direction)]:
                continue
        visited[(path, direction)] = total_score
        for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            new_point = (path[0] + dx, path[1] + dy)
            if (dx, dy) == (-direction[0], -direction[1]) or cave_map[new_point] == "#":
                continue
            if (dx, dy) == direction:
                next_paths.append((new_point, (dx, dy), turns, moves + 1))
            else:
                next_paths.append((new_point, (dx, dy), turns+1, moves + 1))

    return minimum_score


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
