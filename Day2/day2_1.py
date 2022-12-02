import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
rps_dict= {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}
point_dict={
    "W":6,
    "D":3,
    "L":0,
    "R":1,
    "P":2,
    "S":3
}

def check_points(opponent, me):
    if opponent == me:
        return point_dict["D"]
    if (opponent=="R" and me == "S") or (opponent=="S" and me == "P") or (opponent=="P" and me == "R"):
        return point_dict["L"]
    else:
        return point_dict["W"]


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    sum_points = 0
    for line in data:
        opponent, me = line.split(" ")
        my_toss = rps_dict[me]
        opponent_toss = rps_dict[opponent]
        sum_points += point_dict[my_toss]
        sum_points += check_points(opponent_toss, my_toss)

    return sum_points


@timeexecution
def execution():
    submit_answer = True
    my_answer = get_my_answer()
    this_day = int(str(filepath).split("\\")[-1][3:])
    print(my_answer)
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
