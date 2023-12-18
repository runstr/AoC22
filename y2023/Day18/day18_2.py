import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
from matplotlib import pyplot as plt

dir_map = {0: "R", 1: "D", 2: "L",  3: "U"}


def shoelace_formula(coordinates):
    # A function to apply the Shoelace algorithm
    sum = 0
    total_points = len(coordinates)
    j = len(coordinates)-1
    for i in range(0, total_points):
        sum += (coordinates[j][1]+coordinates[i][1])*(coordinates[j][0]-coordinates[i][0])
        j=i
    area = abs(sum) / 2
    return area

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    instructions = []
    for line in data:
        direction, _, RGBcode = line.split()
        length = int(RGBcode[2:-2], 16)
        direction = RGBcode[-2]
        direction = dir_map[int(direction)]
        instructions.append((direction, length))
    map_points = [(0,0)]
    current_x = 0
    current_y = 0
    circumference = 0
    for direction, length in instructions:
        circumference+=length
        if direction == "L":
            dx, dy = -1, 0
        elif direction == "R":
            dx, dy = 1, 0
        elif direction == "U":
            dx, dy = 0, -1
        else:
            dx, dy = 0, 1
        current_x += dx*length
        current_y += dy*length
        map_points.append((current_x, current_y))
    xs = [x[0] for x in map_points]
    ys = [x[1] for x in map_points]
    plt.plot(xs, ys)
    area = shoelace_formula(map_points) + circumference/2 +1
    return area



@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
