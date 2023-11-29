import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_region(x, y):
    if (50 <= x < 100) and y < 50:
        return 1
    if (x >= 100) and y < 50:
        return 2
    if (50 <= x < 100) and (50 <= y < 100):
        return 3
    if (50 <= x < 100) and (100 <= y < 150):
        return 4
    if x < 50 and (100 <= y < 150):
        return 5
    if x < 50 and (150 <= y < 200):
        return 6
    raise Exception("coordinate outside region")


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


def map_coords_to_region_coords(coordinates):
    regions_to_map = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    map_to_region = {}
    for coord, (point, region) in coordinates.items():
        if region == 1:
            region_coords = (coord[0]-50, coord[1])
            regions_to_map[1][region_coords] = coord
            pass
        elif region == 2:
            region_coords = (coord[0]-100, coord[1])
            regions_to_map[2][region_coords] = coord
        elif region == 3:
            region_coords = (coord[0]-50, coord[1]-50)
            regions_to_map[3][region_coords] = coord
        elif region == 4:
            region_coords = (coord[0]-50, coord[1]-100)
            regions_to_map[4][region_coords] = coord
        elif region == 5:
            region_coords = (coord[0], coord[1]-100)
            regions_to_map[5][region_coords] = coord
        elif region == 6:
            region_coords = (coord[0], coord[1]-150)
            regions_to_map[6][region_coords] = coord
        else:
            raise Exception("Something went wrong when mapping region coords.")

        map_to_region[coord] = region_coords
    return regions_to_map, map_to_region



def print_map(coordinates, current_point=None, direction=None, coord_to_regions=None):
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
        elif coord_to_regions:
            print(coord_to_regions[coord], end="")
        else:
            print(point[0], end="")


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
    return numbers, directions


def map_edge_to_new_point_and_direction(region, coord, direction, region_to_map, map_to_region):
    coord = map_to_region[coord]
    if region == 1:
        if direction == "N":
            new_region = 6
            x = 0
            y = coord[0]
            new_direction = "E"
        elif direction == "W":
            new_region = 5
            x = 0
            y = 49-coord[1]
            new_direction = "E"
        else:
            raise Exception("Moving in wrong direction for region 1")

    elif region == 2:
        if direction == "N":
            new_region = 6
            x = coord[0]
            y = 49
            new_direction = "N"
        elif direction == "E":
            new_region = 4
            x = 49
            y = 49-coord[1]
            new_direction = "W"
        elif direction == "S":
            new_region = 3
            x = 49
            y = coord[0]
            new_direction = "W"
        else:
            raise Exception("Moving in wrong direction for region 2")

    elif region == 3:
        if direction == "W":
            new_region = 5
            x = coord[1]
            y = 0
            new_direction = "S"
        elif direction == "E":
            new_region = 2
            x = coord[1]
            y = 49
            new_direction = "N"
        else:
            raise Exception("Moving in wrong direction for region 3")

    elif region == 4:
        if direction == "E":
            new_region = 2
            x = 49
            y = 49-coord[1]
            new_direction = "W"
        elif direction == "S":
            new_region = 6
            x = 49
            y = coord[0]
            new_direction = "W"
        else:
            raise Exception("Moving in wrong direction for region 4")

    elif region == 5:
        if direction == "N":
            new_region = 3
            x = 0
            y = coord[0]
            new_direction = "E"
        elif direction == "W":
            new_region = 1
            x = 0
            y = 49-coord[1]
            new_direction = "E"
        else:
            raise Exception("Moving in wrong direction for region 5")

    elif region == 6:
        if direction == "W":
            new_region = 1
            x = coord[1]
            y = 0
            new_direction = "S"
        elif direction == "E":
            new_region = 4
            x = coord[1]
            y = 49
            new_direction = "N"
        elif direction == "S":
            new_region = 2
            x = coord[0]
            y = 0
            new_direction = "S"
        else:
            raise Exception("Moving in wrong direction for region 6")
    else:
        raise Exception("Region does not exist")
    new_coordinates = region_to_map[new_region][(x, y)]
    return new_coordinates, new_direction, new_region


def get_new_direction(current_direction, turn):
    left_turn = {"E": "N", "N": "W", "W": "S", "S": "E"}
    right_turn = {"E": "S", "S": "W", "W": "N", "N": "E"}
    if turn == "L":
        return left_turn[current_direction]
    else:
        return right_turn[current_direction]


def move_person(moves, current_tile, coordinates, direction, region_to_map, map_to_region):
    direction_change = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    last_tile = current_tile
    new_direction = direction
    for j in range(1, moves + 1):
        last_direction = new_direction
        dx, dy = direction_change[new_direction]
        if (last_tile[0] + dx, last_tile[1]+dy) not in coordinates:
            region = get_region(last_tile[0], last_tile[1])
            next_tile, new_direction, temp_region = map_edge_to_new_point_and_direction(region,
                                                                                        (last_tile[0], last_tile[1]),
                                                                                        last_direction,
                                                                                        region_to_map, map_to_region)
        else:
            next_tile = (last_tile[0] + dx, last_tile[1]+dy)
        if coordinates[next_tile][0] == "#":
            current_tile = last_tile
            new_direction = last_direction
            break
        elif j != moves:
            last_tile = next_tile
            continue
        current_tile = next_tile

    return current_tile, new_direction


def get_my_answer():
    mapping, movement = load_data(filepath, example=False).split("\n\n")
    coordinates, current_tile, max_x, max_y = get_map(mapping)
    regions_to_map, map_to_region = map_coords_to_region_coords(coordinates)
    moves, directions = get_movement(movement)
    current_direction = "E"
    for i in range(len(moves)):
        current_tile, current_direction = move_person(moves[i], current_tile, coordinates, current_direction,
                                                      regions_to_map, map_to_region)
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
