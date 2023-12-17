import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

directions = {}

def get_energized(data, mirrors, start_coordinate, start_direction, max_x, max_y):
    visited = set()
    cordinates = [start_coordinate]
    directions = [start_direction]
    new_map = [list(line) for line in data]
    new_map[start_coordinate[1]][start_coordinate[0]] = "#"
    while cordinates:
        coord = cordinates.pop()
        direction = directions.pop()
        if coord in mirrors:
            mirror = mirrors[coord]
            if mirror == "-":
                if direction[0] == 1 or direction[0] == -1:
                    new_coords = [(coord[0] + direction[0], coord[1])]
                    new_directions = [direction]
                else:
                    new_coords = [(coord[0] + 1, coord[1]), (coord[0] - 1, coord[1])]
                    new_directions = [(+1, 0), (-1, 0)]
            elif mirror == "|":
                if direction[1] == 1 or direction[1] == -1:
                    new_coords = [(coord[0], coord[1] + direction[1])]
                    new_directions = [direction]
                else:
                    new_coords = [(coord[0], coord[1] + 1), (coord[0], coord[1] - 1)]
                    new_directions = [(0, 1), (0, -1)]
            elif mirror == "/":
                if direction[0] == 1:
                    new_coords = [(coord[0], coord[1] - 1)]
                    new_directions = [(0, -1)]
                elif direction[0] == -1:
                    new_coords = [(coord[0], coord[1] + 1)]
                    new_directions = [(0, 1)]
                elif direction[1] == 1:
                    new_coords = [(coord[0] - 1, coord[1])]
                    new_directions = [(-1, 0)]
                else:
                    new_coords = [(coord[0] + 1, coord[1])]
                    new_directions = [(1, 0)]
            elif mirror == "\\":
                if direction[0] == 1:
                    new_coords = [(coord[0], coord[1] + 1)]
                    new_directions = [(0, 1)]
                elif direction[0] == -1:
                    new_coords = [(coord[0], coord[1] - 1)]
                    new_directions = [(0, -1)]
                elif direction[1] == 1:
                    new_coords = [(coord[0] + 1, coord[1])]
                    new_directions = [(1, 0)]
                else:
                    new_coords = [(coord[0] - 1, coord[1])]
                    new_directions = [(-1, 0)]
        else:
            new_coords = [(coord[0] + direction[0], coord[1] + direction[1])]
            new_directions = [direction]
        for i, new_coordinate in enumerate(new_coords):
            visited_with_dir = (new_coordinate, new_directions[i])
            if visited_with_dir not in visited and new_coordinate[0] < max_x and new_coordinate[0] >= 0 and \
                    new_coordinate[1] < max_y and new_coordinate[1] >= 0:
                visited.add(visited_with_dir)
                cordinates.append(new_coordinate)
                directions.append(new_directions[i])
                new_map[new_coordinate[1]][new_coordinate[0]] = "#"
    total_energized = 0
    for line in new_map:
        #print("".join(line).replace(".", ","))
        total_energized += line.count("#")
    #print()
    return total_energized

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    mirrors = {}
    for y, line in enumerate(data):
        for x, mirror in enumerate(line):
            if mirror != ".":
                mirrors[(x, y)] = mirror
    max_energized = 0
    max_x = len(data[0])
    max_y = len(data)
    start_coordinates = []
    start_directions = []
    for y in range(0, max_y):
        for x in range(0, max_x):
            if x > 0 and y > 0  and x < max_x-1 and y < max_y -1:
                continue
            if x == 0:
                start_coordinates.append((x, y))
                start_directions.append((1, 0))
            if y == 0:
                start_coordinates.append((x, y))
                start_directions.append((0, 1))
            if x == max_x-1:
                start_coordinates.append((x, y))
                start_directions.append((-1, 0))
            if y == max_y-1:
                start_coordinates.append((x, y))
                start_directions.append((0, -1))
    for i in range(len(start_directions)):
        start_c = start_coordinates[i]
        start_d = start_directions[i]
        energized_value = get_energized(data, mirrors, start_c, start_d, max_x, max_y)
        if energized_value > max_energized:
            max_energized = energized_value
    return max_energized


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
