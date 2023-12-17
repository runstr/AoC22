import heapq
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

import math
filepath = pathlib.Path(__file__).parent.resolve()

class Path:
    def __init__(self, start_positions, wiegte):
        current_step  None:
    current_ste
def print_nodes(end_node, max_x, max_y, previous_path):
    new_map = [[","]*max_x for _ in range(max_y)]
    current_node = end_node
    while True:
        new_map[current_node[1]][current_node[0]] = "#"
        try:
            new_node = previous_path[current_node]
            if current_node == new_node:
                break
        except KeyError as e:
            break
        current_node = new_node
    for line in new_map:
        print("".join(line))

def get_adjacent_points(curr_pos, max_y, max_x, direction):
    adjacent_points = []
    previous_step = (curr_pos[0]-direction[0], curr_pos[1]-direction[1])
    for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
        if curr_pos[0] + dx >= 0 and curr_pos[0] + dx < max_x and curr_pos[1] + dy >= 0 and curr_pos[1] + dy < max_y:
            new_pos = (curr_pos[0] + dx, curr_pos[1] + dy)
            if new_pos != previous_step:
                adjacent_points.append((new_pos, (dx, dy)))
    return adjacent_points


def check_previous_steps(previous_path, start_node, direction):
    try:
        first_node = previous_path[start_node]
        second_node = previous_path[first_node]
        third_node = previous_path[second_node]
    except KeyError:
        return True
    first_dir = (start_node[0] - first_node[0], start_node[1] - first_node[1])
    second_dir = (first_node[0] - second_node[0], first_node[1] - second_node[1])
    third_dir = (second_node[0] - third_node[0], second_node[1] - third_node[1])
    if first_dir == second_dir == third_dir == direction:
        return False
    return True

def dijsktra_search(coordinates, weigthed_cords, max_x, max_y):
    current = [((0, 0), (0, 0), 0)]
    visited = set()
    previous_path = {}
    while current:
        cur_point, current_direction, count = current.pop()
        visited.add((cur_point, current_direction, count))
        next_points = get_adjacent_points(cur_point, max_x, max_y, current_direction)
        for point, direction in next_points:
            if direction == current_direction:
                new_count = count+1
            else:
                new_count = 1
            if new_count > 3:
                continue
            if (point, direction, new_count) in visited:
                continue
            current.append((point, direction, new_count))
            if weigthed_cords[cur_point] + coordinates[point] <= weigthed_cords[point] and check_previous_steps(previous_path, cur_point, direction):
                weigthed_cords[point] = weigthed_cords[cur_point] + coordinates[point]
                previous_path[point] = cur_point
                #print_nodes(cur_point, max_x, max_y, previous_path)
                #print()
    print_nodes((max_x-1, max_y-1), max_x, max_y, previous_path)
    print()



def get_my_answer():
    data = load_data_as_int(filepath, example=True)
    coordinates = {}
    for y, line in enumerate(data):
        for x, weigth in enumerate(line):
            coordinates[(x, y)] = weigth
    weigthed_cords = {}
    for coord in coordinates:
        weigthed_cords[coord] = math.inf
    weigthed_cords[(0, 0)] = 0
    max_x, max_y = len(data[0]), len(data)
    dijsktra_search(coordinates, weigthed_cords, max_x, max_y)
    print(weigthed_cords[(max_y-1,max_y-1)])
    return


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
