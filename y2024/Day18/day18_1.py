import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    example = False
    data = load_data_as_lines(filepath, example=example)
    bitmap = set()
    start_point = (0,0)
    if example:
        max_x = 6
        max_y = 6
        end_point = (6, 6)
        byte_drops = 12
    else:
        max_x = 70
        max_y = 70
        end_point = (70, 70)
        byte_drops = 2987
    for i, point in enumerate(data):
        bitmap.add(tuple(map(int, point.split(","))))
    return run_bfs(bitmap, start_point, end_point, max_x, max_y)


def run_bfs(bitmap, start_point, end_point, max_x, max_y):
    visited = set()
    next_paths = [(start_point, 0)]
    minimum_score = math.inf
    while next_paths:
        point, moves = next_paths.pop(0)
        if moves > minimum_score and moves + check_difference(point, end_point) > minimum_score:
            continue
        if point == end_point:
            if moves < minimum_score:
                minimum_score = moves
            continue
        if point in visited:
            continue
        visited.add(point)
        for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            new_point = (point[0] + dx, point[1] + dy)
            if new_point in bitmap or new_point[0] < 0 or new_point[1] < 0 or new_point[0] > max_x or new_point[1] > max_y:
                continue
            next_paths.append((new_point, moves+1))
    return minimum_score


def check_difference(this_point, other_point):
    dx = this_point[0] - other_point[0]
    dy = this_point[1] - other_point[1]
    minimum_difference = abs(dx) + abs(dy)
    return minimum_difference

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
