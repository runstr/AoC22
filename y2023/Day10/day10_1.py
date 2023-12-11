import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
MAXIMUM_NUMBER = 1

def verify_point(this_point, point, path_lengths, data, allowed_letters):
    if point in path_lengths and path_lengths[this_point]+1>path_lengths[point]:
        return False
    if point[0] > len(data[0]) or point[0] < 0 or point[1] > len(data[-1]) or point[1] < 0:
        return False
    if data[point[1]][point[0]] not in allowed_letters:
        return False
    return True


def find_next_points(this_point, this_letter, path_lengths, data):
    verified_points = []
    if this_letter == "S":
        point1 = (this_point[0], this_point[1]-1)
        point2 = (this_point[0], this_point[1]+1)
        point3 = (this_point[0]-1, this_point[1])
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point, point1, path_lengths, data, allowed_letters=["F", "|", "7"]):
            verified_points.append(point1)
        if verify_point(this_point,point2, path_lengths, data, allowed_letters=["J", "|", "L"]):
            verified_points.append(point2)
        if verify_point(this_point,point3, path_lengths, data, allowed_letters=["F", "-", "L"]):
            verified_points.append(point3)
        if verify_point(this_point,point4, path_lengths, data, allowed_letters=["J", "-", "7"]):
            verified_points.append(point4)
    elif this_letter == "|":
        point1 = (this_point[0], this_point[1]-1)
        point2 = (this_point[0], this_point[1]+1)
        if verify_point(this_point, point1, path_lengths, data, allowed_letters=["F", "|", "7"]):
            verified_points.append(point1)
        if verify_point(this_point, point2, path_lengths, data, allowed_letters=["J", "|", "L"]):
            verified_points.append(point2)
    elif this_letter == "-":
        point3 = (this_point[0]-1, this_point[1])
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point,point3, path_lengths, data, allowed_letters=["F", "-", "L"]):
            verified_points.append(point3)
        if verify_point(this_point,point4, path_lengths, data, allowed_letters=["J", "-", "7"]):
            verified_points.append(point4)
    elif this_letter == "F":
        point2 = (this_point[0], this_point[1]+1)
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point,point2, path_lengths, data, allowed_letters=["J", "|", "L"]):
            verified_points.append(point2)
        if verify_point(this_point,point4, path_lengths, data, allowed_letters=["J", "-", "7"]):
            verified_points.append(point4)
    elif this_letter == "J":
        point1 = (this_point[0], this_point[1]-1)
        point3 = (this_point[0]-1, this_point[1])
        if verify_point(this_point,point1, path_lengths, data, allowed_letters=["F", "|", "7"]):
            verified_points.append(point1)
        if verify_point(this_point,point3, path_lengths, data, allowed_letters=["F", "-", "L"]):
            verified_points.append(point3)
    elif this_letter == "7":
        point2 = (this_point[0], this_point[1]+1)
        point3 = (this_point[0]-1, this_point[1])
        if verify_point(this_point,point2, path_lengths, data, allowed_letters=["J", "|", "L"]):
            verified_points.append(point2)
        if verify_point(this_point,point3, path_lengths, data, allowed_letters=["F", "-", "L"]):
            verified_points.append(point3)
    elif this_letter == "L":
        point1 = (this_point[0], this_point[1]-1)
        point4 = (this_point[0]+1, this_point[1])
        if verify_point(this_point,point1, path_lengths, data, allowed_letters=["F", "|", "7"]):
            verified_points.append(point1)
        if verify_point(this_point,point4, path_lengths, data, allowed_letters=["J", "-", "7"]):
            verified_points.append(point4)
    return verified_points

def recursive_method(this_point, path_lengths, this_letter, data):
    global MAXIMUM_NUMBER
    next_points = find_next_points(this_point=this_point, path_lengths=path_lengths, this_letter=this_letter, data=data)
    for point in next_points:
        new_path_length = path_lengths[this_point]+1
        path_lengths[point] = new_path_length
        letter = data[point[1]][point[0]]
        recursive_method(point, path_lengths, letter, data)
    return


def get_my_answer():
    global MAXIMUM_NUMBER
    data = load_data_as_lines(filepath, example=False)
    start_point = None
    for y, line in enumerate(data):
        x = line.find("S")
        if x >= 0:
            start_point = (x, y)
            break
    path_lengths = {start_point: 0}
    next_points = find_next_points(this_point=start_point, path_lengths=path_lengths, this_letter="S", data=data)
    for point in next_points:
        path_lengths[point] = 1
        while True:
            letter = data[point[1]][point[0]]
            points = find_next_points(this_point=point, path_lengths=path_lengths, this_letter=letter, data=data)
            if not points:
                break
            new_point = points[0]
            new_path_length = path_lengths[point] + 1
            path_lengths[new_point] = new_path_length
            point = new_point
    return max(list(path_lengths.values()))


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
