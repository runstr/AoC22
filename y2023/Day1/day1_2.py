import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

letter_numbers = {"one": 1, "two": 2,"three": 3,"four": 4,"five": 5,"six": 6,"seven": 7,"eight": 8,"nine": 9, "zero": 0}

def check_if_part_of_string(string, reversed):
    for key in letter_numbers.keys():
        if not reversed:
            if string == key[0:len(string)]:
                return True
        else:
            if string == key[::-1][0:len(string)]:
                return True

    return False


def get_my_answer():
    #all_data = load_data(filepath, example=True)
    all_data = load_data_as_lines(filepath, example=False)
    numbers = []
    for data in all_data:
        digit = ""
        for i in range(0, len(data)):
            if data[i].isdigit():
                first = data[i]
                break
            else:
                digit += data[i]
                if not check_if_part_of_string(digit, reversed=False):
                    digit = data[i]
                    continue
                try:
                    first = str(letter_numbers[digit])
                    break
                except KeyError:
                    pass
        digit = ""
        for j in range(len(data)-1, -1, -1):
            if data[j].isdigit():
                last = data[j]
                break
            else:
                digit += data[j]
                if not check_if_part_of_string(digit, reversed=True):
                    digit = data[j]
                    continue
                try:
                    last = str(letter_numbers[digit[::-1]])
                    break
                except KeyError:
                    pass


        numbers.append(int(first+last))
    return sum(numbers)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
