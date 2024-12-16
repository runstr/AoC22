import copy
import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
from .day16_1 import run_bfs
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():

    data = load_data_as_lines(filepath, example=False)
    cave_map = {}
    start_point = ()
    end_point = ()
    for y in range(len(data)):
        for x in range(len(data[0])):
            cave_map[(x, y)] = data[y][x]
            if data[y][x] == "S":
                start_point = (x, y)
            if data[y][x] == "E":
                end_point = (x, y)
    minimum_score = run_bfs(cave_map, start_point, end_point)
    visited = dict()
    next_paths = [(start_point, (1, 0), 0, 0, str(start_point)+":")]
    all_paths = []
    while next_paths:
        path, direction, turns, moves, full_path = next_paths.pop(0)
        total_score = turns*1000 + moves
        if total_score > minimum_score or total_score + check_difference(path, end_point) > minimum_score:
            continue
        if cave_map[path] == "E":
            if total_score == minimum_score:
                all_paths.append(full_path)
            continue
        if (path, direction) in visited:
            if total_score > visited[(path, direction)]:
                continue
        visited[(path, direction)] = total_score
        for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            if (dx, dy) == (-direction[0], -direction[1]):
                continue
            new_point = (path[0]+dx, path[1]+dy)
            if cave_map[new_point] == "#":
                continue
            if (dx, dy) == direction:
                next_paths.append((new_point, (dx, dy), turns, moves+1, full_path + str(new_point) + ":"))

            else:
                next_paths.append((new_point, (dx, dy), turns+1, moves+1, full_path + str(new_point) + ":"))

    paths = set()
    for path in all_paths:
        all_points = path.split(":")
        for point in all_points:
            try:
                x, y = tuple(map(int,(point[1:-1].split(", "))))
                paths.add((x, y))
            except:
                pass

    return len(paths)

def check_difference(this_point, other_point):
    dx = this_point[0] - other_point[0]
    dy = this_point[1] - other_point[1]
    minimum_difference = abs(dx) + abs(dy)
    if dx == 0 or dy == 0:
        return minimum_difference
    else:
        return minimum_difference +1000
@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
