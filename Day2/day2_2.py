import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
rps_dict= {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "L",
    "Y": "D",
    "Z": "W",
}
point_dict={
    "W": 6,
    "D": 3,
    "L": 0,
    "R": 1,
    "P": 2,
    "S": 3
}

def check_toss(opponent, end_result):
    if end_result == "D":
        return opponent
    if end_result == "L":
        if opponent=="R":
            return "S"
        elif opponent=="S":
            return "P"
        elif opponent=="P":
            return "R"
    else:
        if opponent == "R":
            return "P"
        elif opponent == "S":
            return "R"
        elif opponent == "P":
            return "S"


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    sum_points = 0
    for line in data:
        opponent, result = line.split(" ")
        end_result = rps_dict[result]
        opponent_toss = rps_dict[opponent]
        sum_points += point_dict[end_result]
        sum_points += point_dict[check_toss(opponent_toss, end_result)]

    return sum_points


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    this_day = int(str(filepath).split("\\")[-1][3:])
    print(my_answer)
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
