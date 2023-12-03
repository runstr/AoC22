import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
def calculate_bounding_box(start, end, max_x, max_y):
    """
    Find bounding box of a given line
    :param start: start coordinate of line
    :param end: end coordinate of line
    :param max_x: highest x coordinate
    :param max_y: highest y coordinate
    :return: List of all coordinates of bounding elements
    """
    bounding_indexes = []
    for x in range(start[0]-1, end[0]+2):
        if x < 0 or x > max_x:
            continue
        for y in range(start[1] - 1, end[1] + 2):
            if y < 0 or y > max_y:
                continue
            bounding_indexes.append((x,y))
    return bounding_indexes

def evaulate_data(data):
    numbers, symbol_indexes = [], []
    y = 0
    for line in data:
        number = ""
        start_index = -1
        started_number = False
        for x, step in enumerate(line):
            if step.isdigit():
                if not started_number:
                    started_number = True
                    start_index = x
                number += step
                continue
            if started_number:
                started_number = False
                end_index = x-1
                numbers.append((int(number), (start_index, y), (end_index, y)))
                number = ""
            if step != ".":
                symbol_indexes.append((x, y))
        if started_number:
            end_index = x - 1
            numbers.append((int(number), (start_index, y), (end_index, y)))
        y+=1
    max_x, max_y = x, y
    return numbers, symbol_indexes, max_x, max_y

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    numbers, symbol_indexes, max_x, max_y = evaulate_data(data)
    all_numbers = []
    for num, start, end in numbers:
        bounding_box = calculate_bounding_box(start, end, max_x, max_y)
        for i in bounding_box:
            if i in symbol_indexes:
                all_numbers.append(num)
                break

    return numbers, symbol_indexes, all_numbers


@timeexecution
def execution():
    submit_answer = False
    numbers, symbol_indexes, all_numbers = get_my_answer()
    print(numbers)
    print(symbol_indexes)
    print(all_numbers)
    for number in all_numbers:
        if number >= 1000:
            print("WRONG")
    my_answer = sum(all_numbers)
    print(sum(all_numbers))
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
