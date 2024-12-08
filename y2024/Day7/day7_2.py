import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def ternary (n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def check_number(answer, parameters, ternary_string):
    equation = parameters[0]
    for i in range(1, len( parameters)):
        if ternary_string[i-1]=="0":
            equation=equation+parameters[i]
        elif ternary_string[i - 1] == "1":
            equation = int(str(equation) + str(parameters[i]))
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
        for i in range(0, 3 ** (len(parameters) - 1)):
            ternary_string = ternary(i)
            ternary_string=ternary_string.zfill(len(parameters)-1)
            if check_number(answer, parameters, ternary_string):
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
        submit(my_answer, part="b", day=this_day, year=2024)
