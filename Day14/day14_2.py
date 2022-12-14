import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
import math


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
            if point[0] < min_x:
                min_x = point[0]
            elif point[0] > max_x:
                max_x = point[0]
            if next_point[0] < min_x:
                min_x = next_point[0]
            elif next_point[0] > max_x:
                max_x = next_point[0]
            if point[1] < min_y:
                min_y = point[1]
            elif point[1] > max_y:
                max_y = point[1]
            if next_point[1] < min_y:
                min_y = next_point[1]
            elif next_point[1] > max_y:
                max_y = next_point[1]
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
    max_y = max_y+2
    #print_rocks(rocks, min_x, max_x, min_y, max_y)
    found_end = False
    last_sand = (500, 0)
    while True:
        sand = last_sand
        while True:
            if sand[1]+1 == max_y:
                rocks[(sand[0], max_y)] = "#"
                rocks[(sand[0] + 1, max_y)] = "#"
                rocks[(sand[0] - 1, max_y)] = "#"
                rocks[(sand[0] + 2, max_y)] = "#"
                rocks[(sand[0] - 2, max_y)] = "#"
            if (sand[0], sand[1]+1) not in rocks:
                sand = (sand[0], sand[1]+1)
                continue
            elif (sand[0]-1, sand[1]+1) not in rocks:
                sand = (sand[0] - 1, sand[1]+1)
                continue
            elif (sand[0]+1, sand[1]+1) not in rocks:
                sand = (sand[0]+1, sand[1]+1)
                continue
            if sand == (500, 0):
                found_end = True
                break
            rocks[(sand[0], sand[1])] = "o"
            break
        i += 1
        if found_end:
            break
    #print_rocks(rocks, min_x, max_x, min_y, max_y)
    return i


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
