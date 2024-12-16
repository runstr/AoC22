import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
directions = {"<": (-1,0), "v": (0,1), ">": (1,0), "^": (0,-1)}

def get_my_answer():
    data = load_data(filepath, example=False)
    cave_map, movements = data.split("\n\n")
    cave_map = cave_map.split("\n")
    dict_map = {}
    min_x, max_x = 0, len(cave_map[0])-1
    min_y, max_y = 0, len(cave_map) - 1
    for y in range(len(cave_map)):
        for x in range(len(cave_map[0])):
            if cave_map[y][x] == "@":
                start_position = (x,y)
                dict_map[(x, y)] = "."
            else:
                dict_map[(x,y)]=cave_map[y][x]
    new_cave_map=[]
    for i in cave_map:
        new_cave_map.append(list(i))
    print(new_cave_map)
    print(dict_map)
    position = start_position
    movements = movements.replace("\n", "")
    for movement in movements:
        #print_map(new_cave_map)
        direction = directions[movement]
        new_pos = (position[0]+direction[0], position[1]+direction[1])
        if dict_map[new_pos] == ".":
            new_cave_map[position[1]][position[0]] = "."
            new_cave_map[new_pos[1]][new_pos[0]] = "@"
            position = new_pos
            continue
        if dict_map[new_pos] == "#":
            continue
        if dict_map[new_pos] == "O":
            next_pos = check_move_boxes(position, dict_map, direction)
            if next_pos == False:
                continue
            else:
                dict_map[next_pos]="O"
                dict_map[new_pos] = "."
                new_cave_map[next_pos[1]][next_pos[0]] = "O"
                new_cave_map[new_pos[1]][new_pos[0]] = "@"
                new_cave_map[position[1]][position[0]] = "."
                position = new_pos
    print_map(new_cave_map)
    print_dict_map(dict_map, max_x+1, max_y+1)
    total_value =0
    for key, value in dict_map.items():
        if value == "O":
            total_value += (key[1]*100+key[0])
    return total_value

def print_map(cave_map):
    for i in cave_map:
        print("".join(i))

def print_dict_map(dict_map, max_x, max_y):
    new_map = [["." for _ in range(max_x)] for _ in range(max_y)]
    for key, value in dict_map.items():
        try:
            new_map[key[1]][key[0]] = value
        except:
            print(key)
    print_map(new_map)

def check_move_boxes(position, dict_map, direction):
    while True:
        new_pos = (position[0]+direction[0], position[1]+direction[1])
        if dict_map[new_pos] == "O":
            position = new_pos
            continue
        if dict_map[new_pos] == ".":
            return new_pos
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
