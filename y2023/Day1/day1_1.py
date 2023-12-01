import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    #all_data = load_data(filepath, example=True)
    all_data = load_data_as_lines(filepath, example=True)
    numbers = []
    for data in all_data:
        digit = ""
        for i in range(0, len(data)):
            if data[i].isdigit():
                first = data[i]
                break
        for j in range(len(data)-1, -1, -1):
            if data[j].isdigit():
                last = data[j]
                break


        numbers.append(int(first+last))

    #all_data = load_data_as_int(filepath, example=True)
    my_answer = sum(numbers)
    return my_answer


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
