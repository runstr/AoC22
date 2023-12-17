import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

directions = {}

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    mirrors = {}
    for y, line in enumerate(data):
        for x, mirror in enumerate(line):
            if mirror != ".":
                mirrors[(x, y)] = mirror
    max_x = len(data[0])
    max_y = len(data)
    visited = set()
    cordinates =[(0, 0)]
    directions = [(1, 0)]
    new_map = [list(line) for line in data]
    new_map[0][0] = "#"
    while cordinates:
        coord = cordinates.pop()
        direction = directions.pop()
        if coord in mirrors:
            mirror = mirrors[coord]
            if mirror == "-":
                if direction[0] == 1 or direction[0] == -1:
                    new_coords = [(coord[0]+direction[0], coord[1])]
                    new_directions = [direction]
                else:
                    new_coords = [(coord[0] + 1, coord[1]), (coord[0] - 1, coord[1])]
                    new_directions = [(+1, 0), (-1, 0)]
            elif mirror == "|":
                if direction[1] == 1 or direction[1] == -1:
                    new_coords = [(coord[0], coord[1]+direction[1])]
                    new_directions = [direction]
                else:
                    new_coords = [(coord[0], coord[1]+1), (coord[0], coord[1]-1)]
                    new_directions = [(0, 1), (0, -1)]
            elif mirror == "/":
                if direction[0] == 1:
                    new_coords = [(coord[0], coord[1]-1)]
                    new_directions = [(0, -1)]
                elif direction[0] == -1:
                    new_coords = [(coord[0], coord[1] + 1)]
                    new_directions = [(0, 1)]
                elif direction[1] == 1:
                    new_coords = [(coord[0] -1, coord[1])]
                    new_directions = [(-1, 0)]
                else:
                    new_coords = [(coord[0] + 1, coord[1])]
                    new_directions = [(1, 0)]
            elif mirror == "\\":
                if direction[0] == 1:
                    new_coords = [(coord[0], coord[1]+1)]
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
            if visited_with_dir not in visited and new_coordinate[0]<max_x and  new_coordinate[0]>=0 and new_coordinate[1] < max_y and  new_coordinate[1] >= 0:
                visited.add(visited_with_dir)
                cordinates.append(new_coordinate)
                directions.append(new_directions[i])
                new_map[new_coordinate[1]][new_coordinate[0]] = "#"
    total_energized = 0
    for line in new_map:
        print("".join(line).replace(".", ","))
        total_energized+=line.count("#")


    return total_energized


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
