import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    grid = load_data_as_lines(filepath, example=False)
    total_xmas = 0
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] == "A":
                if check_direction_for_mas(x, y, grid):
                    total_xmas += 1

    return total_xmas


def check_direction_for_mas(x, y, grid):
    x1, y1, = x - 1, y - 1
    x2, y2 = x + 1, y - 1
    x3, y3 = x - 1, y + 1
    x4, y4 = x + 1, y + 1
    string = grid[y1][x1] + grid[y2][x2] + grid[y3][x3] + grid[y4][x4]
    allowed_strings = ["MSMS", "SMSM", "SSMM", "MMSS"]
    if string in allowed_strings:
        return True
    return False


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
