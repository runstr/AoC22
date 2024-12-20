import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data(filepath, example=False)
    first, instructions = data.split("\n\n")
    registers = {}
    for i in first.split("\n"):
        reg, val = i.split(": ")
        registers[reg[-1]] = int(val)
    instructions = list(map(int, instructions[9:].split(",")))
    output = ""
    i=0
    while True:
        if i >= len(instructions):
            break
        instruction = instructions[i]
        operand = instructions[i+1]
        match instruction:
            case 0:
                x = translate_operand(operand, registers)
                registers["A"] = int(registers["A"]/2**x)
            case 1:
                registers["B"] = registers["B"] ^ operand
            case 2:
                registers["B"] = translate_operand(operand, registers) % 8
            case 3:
                if registers["A"] != 0:
                    i = operand
                    continue
                    pass
            case 4:
                registers["B"] =registers["B"]^registers["C"]
            case 5:
                output += str(translate_operand(operand, registers)%8)+","
            case 6:
                x = translate_operand(operand, registers)
                registers["B"] = int(registers["A"] / 2 ** x)
            case 7:
                x = translate_operand(operand, registers)
                registers["C"] = int(registers["A"] / 2 ** x)
        i += 2
    print(registers)
    return output


def translate_operand(operand, registers):
    if 0 <= operand <= 3:
        x = operand
    elif operand == 4:
        x = registers["A"]
    elif operand == 5:
        x = registers["B"]
    elif operand == 6:
        x = registers["C"]
    else:
        raise ValueError("Invalid operand")
    return x

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
