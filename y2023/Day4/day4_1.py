import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    total_points = 0
    for line in data:
        card_number, points = line.split(":")
        card_number = int(card_number[4:].removeprefix(" "))
        winning_numbers, numbers = points.split(" | ")
        winning_numbers = winning_numbers.removeprefix(" ").split(" ")
        winning_numbers = [int(winning_number) for winning_number in winning_numbers if winning_number != ""]
        numbers = numbers.removeprefix(" ").split(" ")
        numbers = [int(number) for number in numbers if number != ""]
        i = 0
        for number in numbers:
            if number in winning_numbers:
                i += 1
        if i > 0:
            total_points += 2**(i-1)



    return total_points


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
