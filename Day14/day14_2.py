import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=True)
    rocks = {}
    for line in data:
        points = line.split(" -> ")
        for i in range(len(points)-1):
            point = list(map(int, points[i].split(",")))
            next_point = list(map(int, points[i+1].split(",")))
            rocks[(point[0], point[1])] = "#"

            if point[0] != next_point[0]:
                dx = int((next_point[0]-point[0])/abs(next_point[0]-point[0]))
                for i in range(1, abs(next_point[0]-point[0])+1):
                    rocks[(point[0]+i*dx, point[1])] = "#"

            elif point[1] != next_point[1]:
                dy = int((next_point[1]-point[1])/abs(next_point[1]-point[1]))
                for i in range(1, abs(next_point[1]-point[1])+1):
                    rocks[(point[0], point[1]+i*dy)] = "#"

    print(len(rocks))
    return 0


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
