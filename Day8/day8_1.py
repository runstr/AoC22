import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def traverse_y_direction(trees, y, x, direction, boolean):
    for dy in range(1, len(trees)):
        if (y + direction*dy >= len(trees)) or (y + direction*dy < 0):
            break
        if trees[y][x] <= trees[y + direction*dy][x]:
            boolean = False
            break
    return boolean


def traverse_x_direction(trees, y, x, direction, boolean):
    for dx in range(1, len(trees[0])):
        if (x + direction*dx >= len(trees[0])) or (x + direction*dx < 0):
            break
        if trees[y][x] <= trees[y][x + direction*dx]:
            boolean = False
            break
    return boolean


def get_my_answer():
    trees = load_data_as_int(filepath, example=True)
    visible_trees_int = 0
    for y in range(len(trees)):
        for x in range(len(trees[0])):
            pos_x = traverse_x_direction(trees, y, x, 1, True)
            pos_y = traverse_y_direction(trees, y, x, 1, True)
            neg_x = traverse_x_direction(trees, y, x, -1, True)
            neg_y = traverse_y_direction(trees, y, x, -1, True)
            if neg_y or neg_x or pos_x or pos_y:
                visible_trees_int += 1
    return visible_trees_int


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
