import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

next_positions = {
    "<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)
}
next_dir = {
    "<": "^", ">": "v", "^": ">", "v": "<"
}


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    mapping = {}
    current_pos = (0, 0)
    current_dir = "."
    for y in range(len(data)):
        for x in range(len(data[0])):
            mapping[(x, y)] = data[y][x]
            if data[y][x] in ["<", ">", "^", "v"]:
                current_pos = (x, y)
                current_dir = data[y][x]
    next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
    visited = set()
    visited.add(current_pos)
    while True:
        if current_pos[0] == 0 or current_pos[0] == len(data[0]) - 1 or current_pos[1] == 0 or current_pos[1] == len(
                data) - 1:
            break
        if mapping[next_pos] == "#":
            current_dir = next_dir[current_dir]
            next_pos = (
            current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
            continue
        current_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
        visited.add(current_pos)
        next_pos = (current_pos[0] + next_positions[current_dir][0], current_pos[1] + next_positions[current_dir][1])
    return len(visited)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
