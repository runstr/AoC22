import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def traverse_y_direction(trees, y, x, direction, pos_y):
    for dy in range(1, len(trees)):
        if (y + direction*dy >= len(trees)) or (y + direction*dy < 0):
            break
        pos_y += 1
        if trees[y][x] <= trees[y + direction*dy][x]:
            break
    return pos_y


def traverse_x_direction(trees, y, x, direction, pos_x):
    for dx in range(1, len(trees[0])):
        if (x + direction*dx >= len(trees[0])) or (x + direction*dx < 0):
            break
        pos_x += 1
        if trees[y][x] <= trees[y][x + direction*dx]:
            break
    return pos_x


def get_my_answer():
    trees = load_data_as_int(filepath, example=False)
    visible_trees = [[0 for _ in range(len(trees[0]))] for _ in range(len(trees))]
    for y in range(len(trees)):
        for x in range(len(trees[0])):
            pos_x = traverse_x_direction(trees, y, x, 1, 0)
            pos_y = traverse_y_direction(trees, y, x, 1, 0)
            neg_x = traverse_x_direction(trees, y, x, -1, 0)
            neg_y = traverse_y_direction(trees, y, x, -1, 0)
            visible_trees[y][x] = neg_y * neg_x * pos_y * pos_x
    max_line = 0
    for line in visible_trees:
        if max(line) > max_line:
            max_line = max(line)
    return max_line


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
