import pathlib
from copy import deepcopy

from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

next_positions = {
    "<": (-1, 0), ">":(1, 0), "^": (0,-1), "v":(0,1)
}
next_dir = {
    "<": "^", ">": "v", "^": ">", "v": "<"
}


def check_set_hindrance(visited, mapping, current_pos, current_dir,  max_x, max_y, already_tested):
    placement_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
    if placement_pos in already_tested:
        return False
    old_placement = mapping[placement_pos]
    if old_placement == "#":
        return False
    mapping[placement_pos] = "#"
    next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
    while True:
        if current_pos[0] == 0 or current_pos[0] == max_x or current_pos[1] == 0 or current_pos[1] == max_y:
            break

        if mapping[next_pos] == "#":
            current_dir = next_dir[current_dir]
            visited.add((current_pos[0], current_pos[1], current_dir))
            next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
            continue

        current_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
        if (current_pos[0], current_pos[1], current_dir) in visited:
            mapping[placement_pos] = old_placement
            already_tested.add(placement_pos)
            return placement_pos
        visited.add((current_pos[0], current_pos[1], current_dir))
        next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
    mapping[placement_pos] = old_placement
    already_tested.add(placement_pos)
    return False


def check_if_loop(mapping, placement, start_pos, start_dir, max_x, max_y):
    mapping[placement] = "#"

    next_pos = (start_pos[0] + next_positions[start_dir][0], start_pos[1] + next_positions[start_dir][1])
    current_pos = start_pos
    current_dir = start_dir
    visited = set()
    visited.add((current_pos[0], current_pos[1], current_dir))

    while True:

        if current_pos[0] == 0 or current_pos[0] == max_x or current_pos[1] == 0 or current_pos[1] == max_y:
            mapping[placement] = "."
            return False

        if mapping[next_pos] == "#":
            current_dir = next_dir[current_dir]
            next_pos = (
            current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
            continue
        current_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
        if (current_pos[0], current_pos[1], current_dir) in visited:
            mapping[placement] = "."
            return True
        visited.add((current_pos[0], current_pos[1], current_dir))
        next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    mapping= {}
    current_pos = (0, 0)
    current_dir = "."
    max_x = len(data[0])-1
    max_y = len(data)-1
    for y in range(max_y+1):
        for x in range(max_x+1):
            mapping[(x,y)] = data[y][x]
            if data[y][x] in ["<", ">", "^", "v"]:
                current_pos = (x, y)
                current_dir = data[y][x]
                mapping[(x, y)] = "."
    next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
    visited = set()
    visited.add((current_pos[0], current_pos[1], current_dir))
    placements = set()
    already_tested = set()
    while True:
        if current_pos[0] == 0 or current_pos[0] == max_x or current_pos[1] == 0 or current_pos[1] == max_y:
            break

        if mapping[next_pos] == "#":
            current_dir = next_dir[current_dir]
            next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
            continue
        result = check_set_hindrance(deepcopy(visited), mapping, current_pos, current_dir, max_x, max_y, already_tested)
        if result is not False:
            placements.add(result)
        current_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
        visited.add((current_pos[0], current_pos[1], current_dir))
        next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])

    print(f"placements: {len(placements)}")
    return len(placements)

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
