import pathlib
from copy import copy

from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def get_neighbours(point, traverse_map, current_path):
    possible_paths = []
    for dx, dy in [(1, 0),(-1, 0),(0, 1), (0, -1)]:
        new_point = (point[0] + dx, point[1] + dy)
        try:
            if new_point in current_path:
                continue
            if traverse_map[new_point[1]][new_point[0]] == ".":
                possible_paths.append(new_point)
            elif traverse_map[new_point[1]][new_point[0]] == ">" and dx == 1:
                possible_paths.append(new_point)
            elif traverse_map[new_point[1]][new_point[0]] == "v" and dy == 1:
                possible_paths.append(new_point)
            elif traverse_map[new_point[1]][new_point[0]] == "<" and dx == -1:
                possible_paths.append(new_point)
            elif traverse_map[new_point[1]][new_point[0]] == "^" and dy == -1:
                possible_paths.append(new_point)
        except IndexError as e:
            pass
    return possible_paths

def print_path(traverse_map, path):
    new_traverse_map = copy(traverse_map)
    for point in path:
        new_traverse_map[point[1]] = new_traverse_map[point[1]][:point[0]]+"O"+new_traverse_map[point[1]][point[0]+1:]
    for line in new_traverse_map:
        print(line)

def get_my_answer():
    traverse_map = load_data_as_lines(filepath, example=True)
    start_point = (1, 0)
    current_path = set()
    splits_to_check = [(current_path, start_point)]
    finished_paths = []
    while splits_to_check:
        current_path, next_point = splits_to_check.pop()
        current_path.add(next_point)
        while True:
            new_neighbours = get_neighbours(next_point, traverse_map, current_path)
            if len(new_neighbours) > 1:
                for new_point in new_neighbours:
                    if new_point == (len(traverse_map[0])-2, len(traverse_map)-1):
                        current_path.add(new_point)
                        finished_paths.append(current_path)
                        continue
                    splits_to_check.append((copy(current_path), new_point))
                break
            elif len(new_neighbours) == 1:
                new_point = new_neighbours[0]
                if new_point == (len(traverse_map[0]) - 2, len(traverse_map) - 1):
                    current_path.add(new_point)
                    finished_paths.append(current_path)
                    break
                current_path.add(new_point)
                next_point=new_point
            else:
                break
    max_length = 0
    for path in finished_paths:
        print_path(traverse_map, path)
        print(len(path))
        if len(path) > max_length:
            max_length = len(path)

    return max_length


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
