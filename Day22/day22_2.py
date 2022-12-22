import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def get_region(x, y, w = 50):
    if x < w:
        if y < 3*w:
            return 5
        return 6
    if x < 2*w:
        if y < w:
            return 1
        if y < 2*w:
            return 3
        return 4
    return 2

def get_map(mapping):
    coordinates = {}
    first = False
    beginning_tile = []
    lines = mapping.split("\n")
    max_y = len(lines)-1
    max_x = 0
    for y, line in enumerate(lines):
        max_x = max(max_x, len(line)-1)
        for x, point in enumerate(line):
            if point ==" " or point == "\n":
                continue
            else:
                if not first:
                    beginning_tile = (x, y)
                    first = True
                coordinates[(x, y)] = (point, get_region(x, y))

    return coordinates, beginning_tile, max_x, max_y


def print_map(coordinates, current_point=None, direction=None):
    current_line = -1
    for coord, point in coordinates.items():
        if coord[1] > current_line:
            print()
            print(" "*coord[0], end="")
            current_line = coord[1]
        if coord == current_point:
            print({"N": "^", "S": "v", "W": "<", "E": ">"}[direction], end="")
        elif coord == current_point and point == "#":
            raise Exception("Something has gone wrong")
        else:
            print(point[1], end="")


def get_movement(movement):
    numbers = []
    directions = []
    number = ""
    for i in movement:
        if i.isdigit():
            number += i
        else:
            numbers.append(int(number))
            directions.append(i)
            number = ""
    numbers.append(int(number))
    print(numbers)
    print(directions)
    return numbers, directions


def map_edge_to_new_point_and_direction(coordinates, direction):
    return 0


def get_new_direction(current_direction, turn):
    left_turn = {"E": "N", "N": "W", "W": "S", "S": "E"}
    right_turn = {"E": "S", "S": "W", "W": "N", "N": "E"}
    if turn == "L":
        return left_turn[current_direction]
    else:
        return right_turn[current_direction]


def move_person(moves, current_tile, coordinates, edge_mapping, direction):
    direction_change = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    # edges = {"N": (current_tile[0], x_edges[current_tile[0]][1]),
    #          "S": (current_tile[0], x_edges[current_tile[0]][0]),
    #          "E": (y_edges[current_tile[1]][0], current_tile[1]),
    #          "W": (y_edges[current_tile[1]][1], current_tile[1])}
    dx, dy = direction_change[direction]
    x_edge, y_edge = edge_mapping[direction]
    last_tile = current_tile
    for j in range(1, moves + 1):
        if (last_tile[0] + dx, last_tile[1]+dy) not in coordinates:
            next_tile = (x_edge, y_edge)
        else:
            next_tile = (last_tile[0] + dx, last_tile[1]+dy)
        if coordinates[next_tile] == "#":
            current_tile = last_tile
            break
        elif j != moves:
            last_tile = next_tile
            continue
        current_tile = next_tile

    return current_tile


def get_my_answer():
    mapping, movement = load_data(filepath, example=False).split("\n\n")
    coordinates, current_tile, max_x, max_y = get_map(mapping)
    directions = ["E","W","S","N"]
    print_map(coordinates)
    edge_mapping = map_edge_to_new_point_and_direction(coordinates, directions)
    moves, directions = get_movement(movement)
    current_direction = "E"
    for i in range(len(moves)):
        print(moves[i], current_direction)
        current_tile = move_person(moves[i], current_tile, coordinates, edge_mapping, current_direction)
        #print_map(coordinates, current_tile, current_direction)
        try:
            current_direction = get_new_direction(current_direction, directions[i])
        except IndexError:
            continue
    direction_point_mapping = {"N": 3, "S": 1, "E": 0, "W": 2}

    return 1000*(current_tile[1]+1)+4*(current_tile[0]+1)+direction_point_mapping[current_direction]


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)


"""
mappings: 

1-2: E = Y const, x end to beginning, dir = E
1-3: S = x = const, Y end to beginning, dir = S
1-5: W = y = const, x  = end-x dir  = E
1-6: N = y = yend to x beginning, x  = y = E

osv

"""