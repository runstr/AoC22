import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_neigbours(point, max_x, max_y, map_points):
    new_points = set()
    for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        new_point = (point[0] + dx, point[1] + dy)
        if 0 <= new_point[0] < max_x and 0 <= new_point[1] < max_y:
            if map_points[new_point] != "#":
                new_points.add(new_point)
    return new_points

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    max_x = len(data[0])
    max_y = len(data[0])
    map_points = {}
    for y, line in enumerate(data):
        for x, letter in enumerate(line):
            if letter == "S":
                start_point = (x, y)
            map_points[(x, y)] = letter
    max_steps = 64
    travel_points = [start_point]
    for step in range(max_steps):
        new_points = set()
        for point in travel_points:
            neigbours = get_neigbours(point, max_x,  max_y, map_points)
            new_points |= neigbours
        travel_points = list(new_points)

    return len(travel_points)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
