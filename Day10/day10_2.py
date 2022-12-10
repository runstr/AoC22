import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def set_screen_pixel(cycle, x, screen):
    row = cycle // 40
    column = cycle - row * 40
    sprites = (x+row*40 - 1, x+row*40, x+row*40 + 1)
    if cycle in sprites:
        screen[row][column] = "#"
    else:
        screen[row][column] = " "


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    x = 1
    cycle = 0
    screen = [["#" for _ in range(40)] for _ in range(6)]
    for i, instruction in enumerate(data):
        if instruction == "noop":
            cycle += 1
            set_screen_pixel(cycle-1, x, screen)

        elif instruction[0:4] == "addx":
            for j in [1, 2]:
                if j == 1:
                    cycle += 1
                    set_screen_pixel(cycle-1, x, screen)
                else:
                    cycle += 1
                    set_screen_pixel(cycle-1, x, screen)
                    x += int(instruction.split()[1])
        else:
            print("another instruction")
    for line in screen:
        print(" ".join(line))

    return


@timeexecution
def execution():
    submit_answer = False
    get_my_answer()
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit("RGLRBZAU", part="b", day=this_day, year=2022)
