import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    all_new_lines = []
    new_input = []
    for line in data:
        line = list(map(int, line.split()))
        new_lines = [line]
        while True:
            number_difference = [new_lines[-1][i + 1] - new_lines[-1][i] for i in range(0, len(new_lines[-1]) - 1)]
            new_lines.append(number_difference)
            if not any(number_difference):
                break
        i = len(new_lines)-1
        while i != 0:
            new_lines[i-1].append(new_lines[i-1][-1]+new_lines[i][-1])
            i -= 1
        all_new_lines.append(new_lines)
        new_input.append(new_lines[0])
    my_answer = sum([inp[-1] for inp in new_input])
    return new_input, my_answer

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
