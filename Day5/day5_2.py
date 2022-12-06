import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data(filepath, example=False).split("\n\n")
    crates ={}
    for line in data[0].split("\n"):
        stack = 1
        for i, letter in enumerate(line):
            if (i+1) % 4 == 0:
                stack+=1
            elif letter.isalpha():
                try:
                    crates[stack] += letter
                except KeyError:
                    crates[stack] = letter
    for line in data[1].split("\n"):
        number, rest = line.strip("move").split("from")
        crate1, crate2 = rest.split("to")
        crate1 = int(crate1.strip(" "))
        crate2 = int(crate2.strip(" "))
        number = int(number.strip(" "))
        crates[crate2] = crates[crate1][:number] + crates[crate2]
        crates[crate1] = crates[crate1][number:]
    my_answer = ""
    for i in range(1, len(crates)+1):
        my_answer+=crates[i][0]
    return my_answer


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
