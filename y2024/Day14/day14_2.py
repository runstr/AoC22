import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    max_x = 101
    max_y = 103
    points = []
    for i in data:
        x, y = tuple(map(int, i.split(" ")[0][2:].split(",")))
        dx, dy = tuple(map(int, i.split(" ")[1][2:].split(",")))
        points.append(((x, y), (dx, dy)))
    print(points)
    i=1
    while True:
        new_points = set()
        for point in points:
            x = point[0][0]
            y = point[0][1]
            dx = point[1][0]
            dy = point[1][1]
            new_x = (x + dx * i) % max_x
            new_y = (y + dy * i) % max_y
            new_points.add((new_x, new_y))
        if check_points(new_points):
            print_points(new_points, max_x, max_y)
            return i
        i += 1

def check_points(points):
    visted = set()
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    for point in points:
        if point in visted:
            continue
        total_flood = 1
        new_points = [point]
        while new_points:
            point = new_points.pop(0)
            if point in visted:
                continue
            total_flood+=1
            if total_flood > 20:
                return True
            visted.add(point)
            for dirx, diry in directions:
                next_point = (point[0]+dirx, point[1]+diry)
                if next_point in points:
                    new_points.append(next_point)
    return False





def print_points(points, max_x, max_y):
    for y in range(max_y):
        for x in range(max_x):
            if (x,y) in points:
                print("x",end="")
            else:
                print("-",end="")
        print()




@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
