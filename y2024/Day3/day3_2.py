import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
import re

def get_my_answer():
    all_data = load_data(filepath, example=False)

    expressions = re.finditer(r"mul\((\d+),(\d+)\)", all_data)
    dont_expressions = re.finditer(r"don't\(\)", all_data)
    do_expressions = re.finditer(r"do\(\)", all_data)
    dont_index = dont_expressions.__next__().start()
    do_index = do_expressions.__next__().start()
    total_value = 0
    disabled = False
    for expression in expressions:
        index = expression.start()
        if index > dont_index:
            try:
                disabled = True
                dont_index = dont_expressions.__next__().start()
            except StopIteration:
                dont_index = math.inf
                pass
        if index > do_index:
            try:
                disabled = False
                do_index = do_expressions.__next__().start()
            except StopIteration:
                do_index = math.inf
        if not disabled:
            first, last = expression.groups()
            total_value += int(first) * int(last)
    return total_value


@timeexecution
def execution():
    submit_answer = True
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
