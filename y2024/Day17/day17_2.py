import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data(filepath, example=False)
    first, instructions = data.split("\n\n")
    instructions = list(map(int, instructions[9:].split(",")))
    string_instructions = "".join(map(str, instructions))
    registers = {"A": 0, "B": 0, "C": 0}
    start_values = [("", 0)]
    while True:
        start_value, i = start_values.pop(0)
        for j in range(0, 8):
            value = start_value + bin(j)[2:].zfill(3)
            reg_value = int(value, 2)
            registers["A"] = reg_value
            output = peform_program(instructions, registers).replace(",", "")
            if output[-(i+1)] == string_instructions[-(i+1)]:
                if len(output) == len(string_instructions):
                    return int(value, 2)
                start_values.append((value, i+1))
        if not start_values:
            break


def peform_program(instructions, registers):
    output = ""
    i = 0
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
            case 4:
                registers["B"] =registers["B"]^registers["C"]
            case 5:
                output+=(str(translate_operand(operand, registers)%8)+",")
            case 6:
                x = translate_operand(operand, registers)
                registers["B"] = int(registers["A"] / 2 ** x)
            case 7:
                x = translate_operand(operand, registers)
                registers["C"] = int(registers["A"] / 2 ** x)
        i += 2
    return output[:-1]


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
        submit(my_answer, part="b", day=this_day, year=2024)
