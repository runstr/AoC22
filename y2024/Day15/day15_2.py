import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
directions = {"<": (-1,0), "v": (0,1), ">": (1,0), "^": (0,-1)}

def get_my_answer():
    data = load_data(filepath, example=False)
    cave_map, movements = data.split("\n\n")
    cave_map = cave_map.split("\n")
    max_x = len(cave_map[0])
    max_y = len(cave_map)
    cave_map = create_new_cave_map(cave_map, max_x, max_y)
    max_x = max_x*2
    new_map = {}
    start_position = (0,0)
    for y in range(max_y):
        for x in range(max_x):
            if cave_map[y][x] == "@":
                start_position = (x,y)
                new_map[(x, y)] = "."
            else:
                new_map[(x,y)]=cave_map[y][x]
    position = start_position
    movements = movements.replace("\n", "")
    for movement in movements:
        #print_dict_map(new_map, max_x, max_y, position)
        direction = directions[movement]
        #print(direction)
        new_pos = (position[0]+direction[0], position[1]+direction[1])
        if new_map[new_pos] == ".":
            position = new_pos
            continue
        if new_map[new_pos] == "#":
            continue
        if new_map[new_pos] == "[" or new_map[new_pos] == "]":
            if direction in [(-1,0),(1,0)]:
                new_positions = check_x_direction(position, new_map, direction)
                if new_positions:
                    for pos, val in new_positions.items():
                        new_map[pos] = val
                    position = new_pos
                else:
                    continue
            else:
                new_positions = check_y_direction(position, new_map, direction)
                if new_positions:
                    for pos, val in new_positions.items():
                        new_map[pos] = val
                    position = new_pos
                else:
                    continue
    print_dict_map(new_map, max_x, max_y, position)
    total_value =0
    for key, value in new_map.items():
        if value == "[":
            total_value += (key[1]*100+key[0])
    return total_value

def create_new_cave_map(cave_map, max_x, max_y):
    new_map = []
    for y in range(0, max_y):
        x_map = ""
        for x in range(0, max_x):
            if cave_map[y][x] == ".":
                x_map+=".."
            elif cave_map[y][x] == "O":
                x_map+="[]"
            elif cave_map[y][x] == "#":
                x_map+="##"
            else:
                x_map += "@."
        new_map.append(list(x_map))
    return new_map



def print_map(cave_map):
    for i in cave_map:
        print("".join(i))

def print_dict_map(dict_map, max_x, max_y, robot_position):
    new_map = [["." for _ in range(max_x)] for _ in range(max_y)]
    for key, value in dict_map.items():
        if key == robot_position:
            new_map[key[1]][key[0]] = "@"
        else:
            new_map[key[1]][key[0]] = value
    print_map(new_map)

def check_y_direction(position, dict_map, direction):
    visited = set()
    new_positions = {}
    new_pos = (position[0], position[1]+direction[1])
    moved = set()
    next_positions = [new_pos]
    if dict_map[new_pos] == "[":
        next_positions.append((position[0] + 1, position[1] + direction[1]))
    else:
        next_positions.append((position[0] - 1, position[1] + direction[1]))
    while next_positions:
        new_pos = next_positions.pop(0)
        if dict_map[new_pos] == "#":
            return False
        if new_pos in visited:
            continue
        visited.add(new_pos)
        if dict_map[new_pos] == ".":
            continue
        moved.add((new_pos[0], new_pos[1]))
        next_pos = (new_pos[0], new_pos[1] + direction[1])
        next_positions.append(next_pos)
        if dict_map[next_pos] == "[":
            next_positions.append((next_pos[0] + 1, next_pos[1]))
        elif dict_map[next_pos] == "]":
            next_positions.append((next_pos[0] - 1, next_pos[1]))

    for move in moved:
        new_positions[(move[0], move[1] + direction[1])] = dict_map[(move[0], move[1])]
    for move in moved:
        if move not in new_positions:
            new_positions[move] = "."
    return new_positions

def check_x_direction(position, dict_map, direction):
    new_dict = {position: "."}
    while True:
        new_pos = (position[0]+direction[0], position[1]+direction[1])
        new_dict[new_pos] = dict_map[position]
        if dict_map[new_pos] == "[" or dict_map[new_pos] == "]":
            position = new_pos
            continue
        if dict_map[new_pos] == ".":
            return new_dict
        if dict_map[new_pos] == "#":
            return False

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
