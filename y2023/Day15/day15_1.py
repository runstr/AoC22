import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data(filepath, example=False)
    all_sums = []
    for line in data.split(","):
        this_sum = 0
        for letter in line:
            this_sum += ord(letter)
            this_sum *= 17
            this_sum = this_sum % 256
        all_sums.append(this_sum)

    return sum(all_sums)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
