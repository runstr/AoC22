import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def adjacent_cubes(cube, cubes):
    adjacent = 0
    for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
        if (cube[0]+dx, cube[1]+dy, cube[2]+dz) in cubes:
            adjacent += 1
    return adjacent


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    cubes = {}
    for cube in data:
        cubes[tuple(map(int, cube.split(",")))] = "white"
    exposed_sides = {}
    for cube in cubes:
        exposed_sides[cube] = 6 - adjacent_cubes(cube, cubes)
    return sum(exposed_sides.values())


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
