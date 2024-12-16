import pathlib
import re

from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    max_x = 101
    max_y = 103
    seconds = 100
    middle_x = max_x//2
    middle_y = max_y//2
    quadrants = [((0, middle_x-1), (0, middle_y-1)), ((middle_x+1, max_x), (0, middle_y-1)),
                 ((0, middle_x-1), (middle_y+1, max_y)), ((middle_x+1, max_x), (middle_y+1, max_y))]
    robot_quadrants = [[],[],[],[]]

    for i in data:
        x, y = tuple(map(int, i.split(" ")[0][2:].split(",")))
        dx, dy = tuple(map(int, i.split(" ")[1][2:].split(",")))
        #print(x,y,dx,dy)
        newx = x + dx*100
        newy = y + dy*100
        newx = newx%max_x
        newy = newy%max_y
        #print(newx, newy)
        for i, q in enumerate(quadrants):
            if q[0][0]<=newx<=q[0][1] and q[1][0]<=newy<=q[1][1]:
                robot_quadrants[i].append((newx, newy))
    print(robot_quadrants)

    return len(robot_quadrants[0])*len(robot_quadrants[1])*len(robot_quadrants[2])*len(robot_quadrants[3])


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
