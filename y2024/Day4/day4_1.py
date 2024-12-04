import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    grid = load_data_as_lines(filepath, example=False)
    total_xmas = 0
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            if grid[y][x] == "X":
                total_xmas += check_all_directions(x, y, grid)
    return total_xmas


def check_all_directions(x, y, grid):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    number_of_xmas = 0

    for dir in directions:
        try:
            x1 = x + dir[0]
            y1 = y + dir[1]
            x2 = x + dir[0] * 2
            y2 = y + dir[1] * 2
            x3 = x + dir[0] * 3
            y3 = y + dir[1] * 3
            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x3 < 0 or y3 < 0:
                continue
            if grid[y][x] + grid[y1][x1] + grid[y2][x2] + grid[y3][x3] == "XMAS":
                number_of_xmas += 1
        except Exception as e:
            pass
    return number_of_xmas


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
