import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, load_data_as_chars, timeexecution
import numpy as np
from aocd import submit
from queue import Queue
filepath = pathlib.Path(__file__).parent.resolve()

def find_adjacant(data):
    adjacent = {}
    for y in range(0, len(data)):
        for x in range(0, len(data[0])):
            point = (x, y)
            adjacent_points = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if abs(dy) == 1 and abs(dx) == 1 or (dy == 0 and dx == 0):
                        continue
                    if x+dx < 0 or x+dx >= len(data[0]) or y+dy < 0 or y+dy >= len(data):
                        continue
                    if ord(data[y+dy][x+dx]) <= ord(data[y][x])+1:
                        adjacent_points.append((x+dx, y+dy))
            adjacent[point] = adjacent_points
    return adjacent

def get_my_answer():
    data = np.array(load_data_as_chars(filepath, example=False))
    points = np.where(data == "S")
    startpoint = (points[1][0], points[0][0])
    points = np.where(data == "E")
    endpoint = (points[1][0], points[0][0])
    data[startpoint[1], startpoint[0]] = "a"
    data[endpoint[1], endpoint[0]] = "z"
    adjacant_points = find_adjacant(data)

    visited = set()
    queue = []
    queue.append(startpoint)
    visited.add(startpoint)
    parent = dict()
    parent[startpoint] = None
    # loop until the queue is empty
    while queue:
        current_node = queue.pop(0)
        if current_node == endpoint:
            break
        for neighbour_node in adjacant_points[current_node]:
            if neighbour_node not in visited:
                queue.append(neighbour_node)
                parent[neighbour_node] = current_node
                visited.add(neighbour_node)
    path = []
    target_node = endpoint
    path.append(target_node)
    while parent[target_node] is not None:
        path.append(parent[target_node])
        target_node = parent[target_node]
    return len(path)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
