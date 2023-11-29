import pathlib
import math
from Tools.tools import load_data_as_lines, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_boundry(cubes):
    mins = [math.inf, math.inf, math.inf]
    maxs = [-math.inf, -math.inf, -math.inf]
    for x, y, z in cubes:
        mins = [min(mins[0], x), min(mins[1], y), min(mins[2], z)]
        maxs = [max(maxs[0], x), max(maxs[1], y), max(maxs[2], z)]
    mins = [min_xyz-1 for min_xyz in mins]
    maxs = [max_xyz + 1 for max_xyz in maxs]
    return mins, maxs


def get_all_adjacent_cubes(cube, cubes):
    adjacent = 0
    for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
        if (cube[0]+dx, cube[1]+dy, cube[2]+dz) in cubes:
            adjacent += 1
    return adjacent


def check_outside(cube, cubes, mins, maxs):
    adjacent = []
    for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
        if mins[0] <= cube[0]+dx <= maxs[0] and \
              mins[1] <= cube[1]+dy <= maxs[1] and \
              mins[2] <= cube[2]+dz <= maxs[2] and \
              (cube[0]+dx, cube[1]+dy, cube[2]+dz) not in cubes:
            adjacent.append((cube[0] + dx, cube[1] + dy, cube[2] + dz))
    return adjacent


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    cubes = {}
    for cube in data:
        cubes[tuple(map(int, cube.split(",")))] = "white"
    mins, maxs = get_boundry(cubes)
    outside_cubes = {}
    queue = [(mins[0], mins[1], mins[2])]
    # Find outside cubes
    while queue:
        cube = queue.pop()
        if cube in outside_cubes:
            continue
        outside_cubes[cube] = "black"
        adjacent_cubes = check_outside(cube, cubes, mins, maxs)
        for adjacent_cube in adjacent_cubes:
            if adjacent_cube not in outside_cubes:
                queue.append(adjacent_cube)
    sides = 0
    for cube in cubes:
        sides += get_all_adjacent_cubes(cube, outside_cubes)
    return sides

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
