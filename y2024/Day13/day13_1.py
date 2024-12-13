import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def transfrom_data(data):
    eqA = data.split("\n")[0].split(": ")[1].split(", ")
    eqA = [int(a[2:]) for a in eqA]
    eqB = data.split("\n")[1].split(": ")[1].split(", ")
    eqB = [int(a[2:]) for a in eqB]
    solution = data.split("\n")[2].split(": ")[1].split(", ")
    solution = [int(a[2:]) for a in solution]
    return eqA, eqB, solution

def get_my_answer():
    data = load_data(filepath, example=False)
    prizes = data.split("\n\n")
    total_tokens = 0
    for prize in prizes:
        eqA, eqB, solution = transfrom_data(prize)
        #eqx = eqA[0] + eqB[0] = solution[0]
        #eqy = eqA[1] + eqB[1] = solution[1]
        tokens = []
        for a in range(0, 100):
            for b in range(0, 100):
                 if eqA[0] * a + eqB[0] * b == solution[0] and eqA[1] * a + eqB[1] * b == solution[1]:
                    tokens.append((3*a+b))
        if tokens:
            total_tokens+=min(tokens)


    return total_tokens


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
