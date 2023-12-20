from heapq import heappop, heappush
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

import math
filepath = pathlib.Path(__file__).parent.resolve()

def update_nodes(nodes_to_visit, heat_map, coordinates, direction, value, max_x, max_y):
    new_directions = [(direction[1], direction[0]), (-direction[1], -direction[0])]
    for new_direction in new_directions:
        parent_node = coordinates
        parent_value = value
        dx, dy = new_direction[0], new_direction[1]
        for i in range(1, 11):
            new_pos = (parent_node[0] + i*dx, parent_node[1] + i*dy)
            if 0 <= new_pos[0] < max_x and 0 <= new_pos[1] < max_y:
                new_value = parent_value + heat_map[(new_pos[0], new_pos[1])]
                if i >= 4:
                    heappush(nodes_to_visit, (new_value, (-new_pos[0], -new_pos[1]), (dx, dy)))
                parent_value = new_value

def print_nodes(end_node, max_x, max_y, parents):
    new_map = [[","]*max_x for _ in range(max_y)]
    current_node = end_node
    while current_node != (0,0):
        new_map[current_node[1]][current_node[0]] = "#"
        current_node = parents[current_node]

    for line in new_map:
        print("".join(line))

def dijsktra_search(weigthed_cords, max_x, max_y, heat_map):
    nodes_to_visit = []
    parents = {}
    heappush(nodes_to_visit, (0, (0, 0), (-1, 0)))
    heappush(nodes_to_visit, (0, (0, 0), (0, -1)))
    visited = set()
    final_value = math.inf
    while nodes_to_visit:
        node = heappop(nodes_to_visit)
        value, coordinates, direction = node
        direction = (-direction[0], -direction[1])
        coordinates = (-coordinates[0], -coordinates[1])
        if (coordinates, direction) in visited:
            continue
        else:
            visited.add((coordinates, direction))
        if value <= math.inf:
            weigthed_cords[coordinates] = value
            parents[coordinates] = (coordinates[0] - direction[0], coordinates[1] - direction[1])
        if coordinates == (max_x-1, max_y-1):
            final_value = value
            break
        update_nodes(nodes_to_visit, heat_map, coordinates, direction, value, max_x, max_y)
    test = weigthed_cords[(max_x-1, max_y-1)]
    print(final_value)
    return test

def get_my_answer():
    data = load_data_as_int(filepath, example=False)
    heat_map = {}
    for y, line in enumerate(data):
        for x, weigth in enumerate(line):
            heat_map[(x, y)] = weigth
    weighted_cords = {}
    for coord in heat_map.keys():
        weighted_cords[coord] = None
    max_x, max_y = len(data[0]), len(data)
    dijsktra_search(weighted_cords, max_x, max_y, heat_map)
    return


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
