import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    return list(map(lambda x: [i for i in [i if len(set(x[i-14:i])) == 14 else x.append(letter) for i, letter in enumerate(open(str(filepath)+"\\input.txt", "r").readline())] if i is not None], [[]]))


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
