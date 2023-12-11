import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
MAXIMUM_NUMBER = 1

replace_characters = {"F": "┍", "L": "┗", "7": "┓", "J": "┙", "-": "╾", "|": "╽"}
import sys
def get_inside_point(this_point, next_point, inside_direction):
    if inside_direction == "right":
        if next_point[0] > this_point[0]:
            return (next_point[0], this_point[1]-1)
        if next_point[0] < this_point[0]:
            return (next_point[0], this_point[1]+1)
        if next_point[1] > this_point[1]:
            return (next_point[0]+1, this_point[1])
        if next_point[1] < this_point[1]:
            return (next_point[0]-1, this_point[1])
    elif inside_direction == "left":
        if next_point[0] > this_point[0]:
            return (next_point[0], this_point[1]+1)
        if next_point[0] < this_point[0]:
            return (next_point[0], this_point[1]-1)
        if next_point[1] > this_point[1]:
            return (next_point[0]-1, this_point[1])
        if next_point[1] < this_point[1]:
            return (next_point[0]+1, this_point[1])

def verify_point(this_point, point, path_points, data, allowed_letters):
    if point in path_points:
        return False
    if point[0] > len(data[0]) or point[0] < 0 or point[1] > len(data[-1]) or point[1] < 0:
        return False
    if data[point[1]][point[0]] not in allowed_letters:
        return False
    return True


def find_next_points(this_point, this_letter, path_points, data):
    verified_points = []
    if this_letter == "S":
        point1 = (this_point[0], this_point[1]-1)
        point2 = (this_point[0], this_point[1]+1)
        point3 = (this_point[0]-1, this_point[1])
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point, point1, path_points, data, allowed_letters=["┍", "╽", "┓"]):
            verified_points.append(point1)
        if verify_point(this_point,point2, path_points, data, allowed_letters=["┙", "╽", "┗"]):
            verified_points.append(point2)
        if verify_point(this_point,point3, path_points, data, allowed_letters=["┍", "╾", "┗"]):
            verified_points.append(point3)
        if verify_point(this_point,point4, path_points, data, allowed_letters=["┙", "╾", "┓"]):
            verified_points.append(point4)
    elif this_letter == "╽":
        point1 = (this_point[0], this_point[1]-1)
        point2 = (this_point[0], this_point[1]+1)
        if verify_point(this_point, point1, path_points, data, allowed_letters=["┍", "╽", "┓"]):
            verified_points.append(point1)
        if verify_point(this_point, point2, path_points, data, allowed_letters=["┙", "╽", "┗"]):
            verified_points.append(point2)
    elif this_letter == "╾":
        point3 = (this_point[0]-1, this_point[1])
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point,point3, path_points, data, allowed_letters=["┍", "╾", "┗"]):
            verified_points.append(point3)
        if verify_point(this_point,point4, path_points, data, allowed_letters=["┙", "╾", "┓"]):
            verified_points.append(point4)
    elif this_letter == "┍":
        point2 = (this_point[0], this_point[1]+1)
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point,point2, path_points, data, allowed_letters=["┙", "╽", "┗"]):
            verified_points.append(point2)
        if verify_point(this_point,point4, path_points, data, allowed_letters=["┙", "╾", "┓"]):
            verified_points.append(point4)
    elif this_letter == "┙":
        point1 = (this_point[0], this_point[1]-1)
        point3 = (this_point[0]-1, this_point[1])
        if verify_point(this_point,point1, path_points, data, allowed_letters=["┍", "╽", "┓"]):
            verified_points.append(point1)
        if verify_point(this_point,point3, path_points, data, allowed_letters=["┍", "╾", "┗"]):
            verified_points.append(point3)
    elif this_letter == "┓":
        point2 = (this_point[0], this_point[1]+1)
        point3 = (this_point[0]-1, this_point[1])
        if verify_point(this_point,point2, path_points, data, allowed_letters=["┙", "╽", "┗"]):
            verified_points.append(point2)
        if verify_point(this_point,point3, path_points, data, allowed_letters=["┍", "╾", "┗"]):
            verified_points.append(point3)
    elif this_letter == "┗":
        point1 = (this_point[0], this_point[1]-1)
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point, point1, path_points, data, allowed_letters=["┍", "╽", "┓"]):
            verified_points.append(point1)
        if verify_point(this_point, point4, path_points, data, allowed_letters=["┙", "╾", "┓"]):
            verified_points.append(point4)
    return verified_points

def flood_fill(this_point, new_data):
    if new_data[this_point[1]][this_point[0]] != ".":
        return
    else:
        new_data[this_point[1]] = new_data[this_point[1]][:this_point[0]] + 'I' + new_data[this_point[1]][this_point[0]+1:]
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_point = (this_point[0]+dx, this_point[1]+dy)
            flood_fill(new_point, new_data)

def get_my_answer():
    global MAXIMUM_NUMBER
    data = load_data_as_lines(filepath, example=True)
    new_data = []
    for line in data:
        for key in replace_characters.keys():
            line = line.replace(key, replace_characters[key])
        new_data.append(line)
        data = new_data
    start_point = None
    for y, line in enumerate(data):
        x = line.find("S")
        if x >= 0:
            start_point = (x, y)
            break
    path_points = [start_point]
    point = start_point
    while True:
        letter = data[point[1]][point[0]]
        points = find_next_points(this_point=point, path_points=path_points, this_letter=letter, data=data)
        if not points:
            break
        new_point = points[0]
        path_points.append(new_point)
        point = new_point
    new_data = []
    for y, line in enumerate(data):
        new_line = ""
        for x in range(len(data[0])):
            if (x, y) not in path_points:
                new_line += "."
            else:
                new_line += line[x]
        new_data.append(new_line)
    start_point = None
    next_point = None
    next_point_index = 0
    for y, line in enumerate(data):
        for x in range(len(data[0])):
            if (x, y) in path_points:
                start_point = (x, y)
                next_point_index = path_points.index((x, y)) + 1
                break
        if start_point is not None:
            break
    for line in new_data:
        print(line)
    total_points = len(path_points)
    this_point = start_point
    next_point = path_points[next_point_index]
    if next_point[0]>this_point[0] or next_point[1]<this_point[1]:
        inside_direction = "left"
    else:
        inside_direction = "right"
    while next_point != start_point:
        inside_point = get_inside_point(this_point=this_point, next_point=next_point, inside_direction=inside_direction)
        flood_fill(inside_point, new_data)
        this_point = next_point
        next_point_index += 1
        if next_point_index == total_points:
            next_point_index = 0
        next_point = path_points[next_point_index]
    total_inside_points = 0
    for line in new_data:
        total_inside_points += line.count("I")
    for line in new_data:
        print(line)
    return total_inside_points


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()

    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
