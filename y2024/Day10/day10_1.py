import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    def check_path(height, position, beginning):
        if height == 9:
            trailheads[beginning].add(position)
            return
        for dirx, diry in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (position[0] + dirx, position[1] + diry)
            if (0 <= new_position[0] <= max_x) and (0 <= new_position[1] <= max_y) and (int(data[new_position[1]][new_position[0]]) == (height + 1)):
                check_path(height + 1, new_position, beginning)

    data = load_data_as_lines(filepath, example=False)
    start_positions = []
    max_y, max_x = len(data)-1, len(data[0])-1
    for y in range(max_y+1):
        for x in range(max_x+1):
            if data[y][x] == "0":
                start_positions.append((x,y))
    trailheads = {pos: set() for pos in start_positions}
    for start_position in start_positions:
        check_path(0, start_position, start_position)
    return sum(len(ends) for ends in trailheads.values())


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
