import pathlib
from copy import copy

from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def get_neighbours(point, node_start, traverse_map):
    possible_paths = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_point = (point[0] + dx, point[1] + dy)
        try:
            if new_point != node_start and traverse_map[new_point[1]][new_point[0]] != "#":
                possible_paths.append(new_point)
        except IndexError as e:
            pass
    return possible_paths

def get_my_answer():
    traverse_map = load_data_as_lines(filepath, example=True)
    nodes = {}
    start_point = (1, 0)
    next_point = (1, 1)
    nodes_to_check = [(start_point, next_point)]
    while nodes_to_check:
        node_start, next_point = nodes_to_check.pop(0)
        last_point = node_start
        steps = 1
        while True:
            possible_points = get_neighbours(next_point, last_point, traverse_map)
            if len(possible_points) > 1:
                if next_point not in nodes:
                    for point in possible_points:
                        nodes_to_check.append((next_point, point))
                if node_start in nodes:
                    if (next_point, steps) not in nodes[node_start]:
                        nodes[node_start].append((next_point, steps))
                else:
                    nodes[node_start] = [(next_point, steps)]

                break
            elif len(possible_points) == 1:
                if possible_points[0] == (len(traverse_map[0]) - 2, len(traverse_map) - 1):
                    nodes[node_start] = [(next_point, steps)]
                    end_path, end_length = node_start, steps
                    break
                last_point = next_point
                next_point = possible_points[0]
                steps += 1
            else:
                break
    current_path = {start_point}
    nodes_to_check = [(node, copy(current_path)) for node in nodes[start_point]]
    full_paths = []
    while nodes_to_check:
        (next_node, distance), current_path = nodes_to_check.pop()
        current_path.add(next_node)
        if next_node == end_path:
            full_paths.append((current_path, distance+end_length))
            continue
        next_nodes = nodes[next_node]
        for node, added_distance in next_nodes:
            if node not in current_path:
                nodes_to_check.append(((node, distance+added_distance), copy(current_path)))
    return print(max(full_paths, key=lambda x: x[1])[1] +1)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
