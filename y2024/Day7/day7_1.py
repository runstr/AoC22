import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def check_number(answer, parameters, binary_string):
    equation = parameters[0]
    for i in range(1, len( parameters)):
        if binary_string[i-1]=="0":
            equation=equation+parameters[i]
        else:
            equation = equation * parameters[i]
    return answer==equation


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    equations = []
    for line in data:
        answer, parameters = line.split(": ")
        parameters = tuple(map(int, parameters.split(" ")))
        answer = int(answer)
        equations.append((answer, parameters))
    possible_answer = []
    for equation in equations:
        answer = equation[0]
        parameters = equation[1]
        for i in range(0, 2 ** (len(parameters) - 1)):
            binary_string = bin(i)
            binary_string=binary_string[2:].zfill(len(parameters)-1)
            if check_number(answer, parameters, binary_string):
                possible_answer.append(answer)
                break

    return sum(possible_answer)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
