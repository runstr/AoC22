import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def check_path(current_height, position, max_x, max_y, data, start_position, trailheads):
    if current_height == 9:
        trailheads[start_position].add(position)
        return
    for dirx, diry in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if position[0] + dirx <= max_x and position[0] + dirx >= 0 and position[1] + diry <= max_y and position[1] + diry >= 0:
            if int(data[position[1] + diry][position[0] + dirx]) == (current_height + 1):
                new_position = (position[0] + dirx, position[1] + diry)
                height = current_height+1
                check_path(height, new_position, max_x, max_y, data, start_position, trailheads)

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    start_positions = []
    max_y = len(data) -1
    max_x = len(data[0]) -1
    for y in range(max_y+1):
        for x in range(max_x+1):
            if data[y][x] == "0":
                start_positions.append((x,y))
    trailheads = {}
    for pos in start_positions:
        trailheads[pos]=set()
    print(len(start_positions))
    for start_position in start_positions:
        current_height = 0
        check_path(current_height, start_position, max_x, max_y, data, start_position, trailheads)

    score = 0
    for start_pos, ends in trailheads.items():
        score+=len(ends)
    print(trailheads)
    return score


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
