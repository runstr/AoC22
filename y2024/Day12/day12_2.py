import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution, load_data_as_chars
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
direction_map = {(0, 1): (1,0) , (1, 0): (0, -1), (-1, 0): (0, 1), (0, -1): (-1,0)}
next_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_my_answer():
    data = load_data_as_chars(filepath, example=False)
    regions = []
    visited = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (x, y) in visited:
                continue

            area, boundry = find_area(data, x, y, visited)

            corners = find_sides(boundry)
            regions.append((corners, area))
    total_sum = 0
    for perimiter, area in regions:
        total_sum += perimiter*area
    return total_sum


def find_area(data, x, y, visited):
    current_garden = data[y][x]
    next_points = [(x, y)]
    area = 0
    boundry = {}
    while next_points:
        point = next_points.pop(0)
        if point in visited:
            continue
        area += 1
        visited.add(point)
        for dirx, diry in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_point = (point[0] + dirx, point[1] + diry)
            if new_point[0] < 0 or new_point[0] >= len(data[0]) or new_point[1] < 0 or new_point[1] >= len(data):
                if (dirx, diry) not in boundry:
                    boundry[(dirx, diry)] = set()
                boundry[(dirx,diry)].add(new_point)
                continue
            if data[new_point[1]][new_point[0]] == current_garden:
                next_points.append(new_point)
            else:
                if (dirx, diry) not in boundry:
                    boundry[(dirx, diry)] = set()
                boundry[(dirx,diry)].add(new_point)
    return area, boundry

def find_sides(boundry):
    sides = 0
    for direction, points in boundry.items():
        if direction in [(0, 1), (0, -1)]:
            sides += 1
            points = sorted(points, key=lambda x: x[0])
            points = sorted(points, key=lambda x: x[1])
            for i in range(1, len(points)):
                if points[i] != (points[i-1][0]+1, points[i-1][1]):
                    sides += 1
        else:
            sides += 1
            points = sorted(points, key=lambda x: x[1])
            points = sorted(points, key=lambda x: x[0])
            for i in range(1, len(points)):
                if points[i] != (points[i-1][0], points[i-1][1]+1):
                    sides += 1
    return sides

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
