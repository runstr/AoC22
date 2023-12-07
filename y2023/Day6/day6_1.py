import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import numpy
import math
filepath = pathlib.Path(__file__).parent.resolve()

def get_possible_ways_to_win_analytic(time, record):
    """ solve equation x**2 -time*x + record = 0. To get the record we x to be higher than x1
    less than x2"""
    x1 = math.floor((time - math.sqrt(time**2 - 4*record))/2 +1)
    x2 = math.ceil((time + math.sqrt(time ** 2 - 4 * record)) / 2 -1)
    return len(range(x1, x2+1))


def get_possible_ways_to_win(time, record):
    total_distance = []
    for i in range(time):
        time_left = time-i
        speed = i
        distance = time_left*speed
        total_distance.append(distance)
    wins = 0
    for i in total_distance:
        if i>record:
            wins+=1
    return wins


def get_my_answer():
    time, distance = load_data_as_lines(filepath, example=True)
    time = time.split(" ")
    distance = distance.split(" ")
    time = list(map(int, [i for i in time if i != ""][1:]))
    distance = list(map(int, [i for i in distance if i != ""][1:]))
    possible_ways_to_win = []
    for i in range(len(time)):
        race_time = time[i]
        record_distance = distance[i]
        possible_ways_to_win.append(get_possible_ways_to_win_analytic(race_time, record_distance))
    return possible_ways_to_win


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
