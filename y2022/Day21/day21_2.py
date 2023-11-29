import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import re
from copy import deepcopy
filepath = pathlib.Path(__file__).parent.resolve()
import sympy as sym


def decode_input(data):
    new_data = {}
    for line in data:
        monkey, code = line.split(": ")
        if "+" in code:
            code = code.split(" + ")
            op = "+"
        elif "-" in code:
            code = code.split(" - ")
            op = "-"
        elif "/" in code:
            code = code.split(" / ")
            op = "/"
        elif "*" in code:
            code = code.split(" * ")
            op = "*"
        else:
            new_data[monkey] = [code]
            continue
        code = ["("]+[code[0]]+[")"]+[op]+["("]+[code[1]]+[")"]
        new_data[monkey] = code
    return new_data


def decode_data(decoded_data, new_data):
    only_numbers = False
    while not only_numbers:
        for i, value in enumerate(decoded_data):
            if value == "x":
                continue
            only_numbers = True
            if value == "(" or value == ")" or value == "/" or value == "+" or value == "*" or value == "-":
                continue
            elif value.isdigit():
                continue
            else:
                new_value = new_data[value]
                only_numbers = False
                decoded_data = decoded_data[:i]+new_value+decoded_data[i+1:]
                break
    return decoded_data


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    new_data = decode_input(data)
    decoded_data = new_data["root"]

    left_side = new_data[decoded_data[1]]
    right_side = new_data[decoded_data[-2]]
    x = sym.Symbol('x')
    new_data["humn"] = ["x"]
    right_side = eval("".join(decode_data(deepcopy(right_side), new_data)))
    left_side = eval("".join(decode_data(deepcopy(left_side), new_data)))
    print(left_side)
    print(right_side)
    answer = sym.solve(left_side-right_side, x)
    return answer


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
