import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    x=1
    cycle = 0
    signal_strengths = []
    for instruction in data:
        if instruction == "noop":
            cycle += 1
            if cycle == 20 or ((cycle - 20) % 40 == 0):
                signal_strengths.append(x)
            continue
        elif instruction[0:4] == "addx":
            cycle += 2
            if cycle == 20 or cycle-1 == 20 or ((cycle-20) % 40 == 0) or ((cycle-1-20) % 40 == 0):
                signal_strengths.append(x)
            x += int(instruction.split()[1])
        else:
            print("another instruction")
    signal_strength = 0
    for i in range(0, len(signal_strengths)):
        if i == 0:
            signal_strength += signal_strengths[i]*20
        else:
            signal_strength += signal_strengths[i] * (20+i*40)
    my_answer=signal_strength
    print(signal_strengths)
    return my_answer


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
