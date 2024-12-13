import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import numpy as np
filepath = pathlib.Path(__file__).parent.resolve()

def transfrom_data(data):
    eqA = data.split("\n")[0].split(": ")[1].split(", ")
    eqA = [int(a[2:]) for a in eqA]
    eqB = data.split("\n")[1].split(": ")[1].split(", ")
    eqB = [int(a[2:]) for a in eqB]
    solution = data.split("\n")[2].split(": ")[1].split(", ")
    solution = [int(a[2:]) for a in solution]
    return eqA, eqB, solution

def solve_A(A, B, C, D, E, F):
    return (B*F-E*C)/(B*D-A*E)

def solve_B(A, B, C, D, E, F):
    return (C*D-A*F)/(B*D-A*E)

def get_my_answer2():
    data = load_data(filepath, example=False)
    prizes = data.split("\n\n")
    total_tokens = 0
    for prize in prizes:
        eqA, eqB, solution = transfrom_data(prize)
        solution[0] = 10000000000000 + solution[0]
        solution[1] = 10000000000000 + solution[1]
        a = np.array([[eqA[0], eqB[0]], [eqA[1], eqB[1]]])
        b = np.array([solution[0], solution[1]])
        retval = np.linalg.solve(a, b)
        if abs(retval[0] - round(retval[0], 0)) <0.001 and abs(retval[1] - round(retval[1], 0)) <0.001:
            print(retval[0], retval[1])
            total_tokens += 3*int(round(retval[0], 0)) + int(round(retval[1], 0))
    return total_tokens

def get_my_answer():
    data = load_data(filepath, example=False)
    prizes = data.split("\n\n")
    total_tokens = 0
    for prize in prizes:
        eqA, eqB, solution = transfrom_data(prize)
        solution[0] = 10000000000000 + solution[0]
        solution[1] = 10000000000000 + solution[1]
        A, B, C, D, E, F = eqA[0], eqB[0], solution[0], eqA[1], eqB[1], solution[1]
        A_button = solve_A(A, B, C, D, E, F)
        B_button = solve_B(A, B, C, D, E, F)
        if A_button.is_integer() and B_button.is_integer():
            print(A_button, B_button)
            total_tokens += 3*int(A_button) + int(B_button)
    return total_tokens
@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
