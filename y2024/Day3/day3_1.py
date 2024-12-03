import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import re
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    all_data = load_data(filepath, example=False)
    # Find all occ
    expressions = re.findall(r"mul\((\d+),(\d+)\)", all_data)
    print(expressions)
    total_number = sum(int(a)*int(b) for a, b in expressions)
    return total_number


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
