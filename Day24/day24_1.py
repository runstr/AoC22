import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def make_map(data):
    map_t0 = {}
    max_x = len(data[0])-1
    max_y = len(data)-1
    for y in range(len(data)):
        for x in range(len(data[0])):
            map_t0[(x, y)] = [data[y][x]]
    mapping = {0: map_t0}
    return mapping, max_x, max_y


def update_position(old_position, direction, max_x, max_y):
    dx, dy = {"<": (-1, 0), ">": (1, 0), "^": (0, -1),  "v": (0, 1)}[direction]
    new_position = (old_position[0]+dx, old_position[1]+dy)
    if new_position[0] < 1:
        new_position = (max_x-1, new_position[1])
    elif new_position[0] > max_x-1:
        new_position = (1, new_position[1])
    elif new_position[1] < 1:
        new_position = (new_position[0], max_y-1)
    elif new_position[1] > max_y-1:
        new_position = (new_position[0], 1)
    return new_position


def update_map(mapping, max_x, max_y, start_position, end_position):
    new_map = {}
    for y in range(max_y+1):
        for x in range(max_x+1):
            if x == 0 or x == max_x or y == 0 or y == max_y:
                if (x, y)!= end_position and (x,y)!=start_position:
                    new_map[(x, y)] = ["#"]
                else:
                    new_map[(x, y)] = ["."]
                continue
            if (x, y) not in new_map:
                new_map[(x, y)] = ["."]
            for wind in mapping[(x, y)]:
                if wind in ["<", ">", "^", "v"]:
                    new_position = update_position((x, y), wind, max_x, max_y)
                    if new_position in new_map:
                        new_map[new_position].append(wind)
                        try:
                            new_map[new_position].remove(".")
                        except ValueError:
                            pass
                    else:
                        new_map[new_position] = [wind]
    return new_map


def print_map(mapping, max_x, max_y):
    for y in range(max_y+1):
        for x in range(max_x+1):
            value = mapping[(x, y)]
            if len(value) > 1:
                print(len(value), end="")
            else:
                print(value[0], end="")
        print()

def get_possible_movements(position, mapping, max_x, max_y, start_position, end_position):
    positions= []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
        new_position = (position[0] + dx, position[1] + dy)
        if new_position[0] <= 0 or new_position[0] >= max_x or new_position[1] <= 0 or new_position[1] >= max_y:
            if new_position != start_position and new_position!=end_position:
                continue
        new_position = (position[0]+dx, position[1]+dy)
        if mapping[new_position][0] == ".":
            positions.append(new_position)
    return positions

def bfs(mappings, start_point, end_point, max_x, max_y):
    visited = set()
    queue = []
    startpoint = (start_point[0], start_point[1], 0)
    queue.append(startpoint)
    visited.add(startpoint)
    parent = dict()
    parent[startpoint] = None
    final_time = 0
    # loop until the queue is empty
    while queue:
        current_node = queue.pop(0)
        time = current_node[2]
        next_time = time+1
        position = (current_node[0], current_node[1])
        if next_time not in mappings:
            mappings[next_time] = update_map(mappings[time], max_x, max_y, start_point, end_point)
        if position == end_point:
            final_time=time
            break
        positions = get_possible_movements(position, mappings[next_time], max_x, max_y, start_point, end_point)
        for pos in positions:
            total_position = (pos[0], pos[1], next_time)
            if total_position not in visited:
                queue.append(total_position)
                parent[total_position] = current_node
                visited.add(total_position)
    return parent, final_time

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    start_point = (1, 0)
    end_point = (len(data[0])-2, len(data)-1)
    mappings, max_x, max_y = make_map(data)
    path, final_time = bfs(mappings, start_point, end_point, max_x, max_y)
    return final_time


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
