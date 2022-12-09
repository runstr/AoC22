import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def move_tail_closer(head_position, tail_position, all_tail_positions):
    dx = head_position[0]-tail_position[0]
    dy = head_position[1]-tail_position[1]
    if dx > 1:
        if dy==1:
            tail_position = (tail_position[0]+1, tail_position[1]+1)
        elif dy==-1:
            tail_position = (tail_position[0]+1, tail_position[1]-1)
        elif dy==0:
            tail_position = (tail_position[0] + 1, tail_position[1])
        else:
            raise Exception("Something went wrong in movin tail")
    elif dy>1:
        if dx==1:
            tail_position = (tail_position[0]+1, tail_position[1]+1)
        elif dx==-1:
            tail_position = (tail_position[0]-1, tail_position[1]+1)
        elif dx==0:
            tail_position = (tail_position[0], tail_position[1]+1)
        else:
            raise Exception("Something went wrong in movin tail")
    elif dx<-1:
        if dy==1:
            tail_position = (tail_position[0]-1, tail_position[1]+1)
        elif dy==-1:
            tail_position = (tail_position[0]-1, tail_position[1]-1)
        elif dy==0:
            tail_position = (tail_position[0]-1, tail_position[1])
        else:
            raise Exception("Something went wrong in moving tail")
    elif dy<-1:
        if dx==1:
            tail_position = (tail_position[0]+1, tail_position[1]-1)
        elif dx==-1:
            tail_position = (tail_position[0]-1, tail_position[1]-1)
        elif dx==0:
            tail_position = (tail_position[0], tail_position[1]-1)
        else:
            raise Exception("Something went wrong in movin tail")
    all_tail_positions.add(tail_position)
    return tail_position


def check_tail_position(head_position, tail_position, all_tail_positions):
    if abs(head_position[0]-tail_position[0])>1 or abs(head_position[1]-tail_position[1])>1:
        tail_position = move_tail_closer(head_position, tail_position, all_tail_positions)
    return tail_position


def move_head(movement, head_position, tail_position, all_tail_positions):
    direction, steps = movement.split()
    for i in range(int(steps)):
        if direction == "U":
            head_position = (head_position[0], head_position[1]+1)
        if direction == "D":
            head_position = (head_position[0], head_position[1]-1)
        if direction == "R":
            head_position = (head_position[0]+1, head_position[1])
        if direction == "L":
            head_position = (head_position[0]-1, head_position[1])
        tail_position = check_tail_position(head_position, tail_position, all_tail_positions)
    return head_position, tail_position


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    all_tail_positions = {(0, 0)}
    head_position = (0, 0)
    tail_position = (0, 0)
    for movement in data:
        head_position, tail_position = move_head(movement, head_position, tail_position, all_tail_positions)
    return len(all_tail_positions)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
