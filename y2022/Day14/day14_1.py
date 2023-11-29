import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import math
import time

filepath = pathlib.Path(__file__).parent.resolve()


def print_rocks(rocks, min_x, max_x, min_y, max_y):
    for y in range(min_y, max_y+1):
        print()
        for x in range(min_x, max_x+1):
            try:
                letter = rocks[(x, y)]
                print(letter, end="")
            except KeyError:
                print("-", end="")
    print()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    rocks = {}
    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf

    for line in data:
        points = line.split(" -> ")
        for i in range(len(points)-1):
            point = list(map(int, points[i].split(",")))
            next_point = list(map(int, points[i+1].split(",")))
            rocks[(point[0], point[1])] = "#"
            min_x = min(point[0], min_x)
            min_x = min(next_point[0], min_x)
            max_x = max(point[0], max_x)
            max_x = max(next_point[0], max_x)
            min_y = min(point[0], min_y)
            min_y = min(next_point[0], min_y)
            max_y = max(point[0], max_y)
            max_y = max(next_point[0], max_y)
            if point[0] != next_point[0]:
                dx = int((next_point[0]-point[0])/abs(next_point[0]-point[0]))
                for i in range(1, abs(next_point[0]-point[0])+1):
                    rocks[(point[0]+i*dx, point[1])] = "#"

            elif point[1] != next_point[1]:
                dy = int((next_point[1]-point[1])/abs(next_point[1]-point[1]))
                for i in range(1, abs(next_point[1]-point[1])+1):
                    rocks[(point[0], point[1]+i*dy)] = "#"
    i = 0
    min_y = 0
    print_rocks(rocks, min_x, max_x, min_y, max_y)
    found_end = False
    while True:
        sand = (500, 0)
        while True:
            if sand[0] >= max_x or sand[0] <= min_x or sand[1] >= max_y:
                found_end = True
                break
            if (sand[0], sand[1]+1) not in rocks:
                sand = (sand[0], sand[1]+1)
                continue
            elif (sand[0]-1, sand[1]+1) not in rocks:
                sand = (sand[0] - 1, sand[1]+1)
                continue
            elif (sand[0]+1, sand[1]+1) not in rocks:
                sand = (sand[0]+1, sand[1]+1)
                continue
            rocks[(sand[0], sand[1])] = "o"
            break
        if found_end:
            break
        i += 1
    print_rocks(rocks, min_x, max_x, min_y, max_y)
    return i


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
