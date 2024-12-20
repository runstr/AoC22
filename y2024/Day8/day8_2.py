import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
from math import gcd

def check_antenna(data, antenoids):
    for antenoid in antenoids:
        data[antenoid[1]] = data[antenoid[1]][:antenoid[0]] + "#" + data[antenoid[1]][antenoid[0] + 1:]
    for line in data:
        print(line)
    return antenoids


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    mapping = {}
    max_x = len(data[0])
    max_y = len(data)
    for y in range(max_y):
        for x in range(max_x):
            if data[y][x] != ".":
                try:
                    mapping[data[y][x]].append((x,y))
                except:
                    mapping[data[y][x]] =[(x, y)]
    antenoids = set()
    for antenna, locations in mapping.items():
        for i in range(len(locations)):
            for j in range(len(locations)):
                if i == j:
                    continue
                antenna1 = locations[i]
                antenna2 = locations[j]
                dir = (antenna2[0]-antenna1[0], antenna2[1]-antenna1[1])
                #print(gcd(*dir))
                distance=0
                while True:
                    antenoid = (antenna2[0]+dir[0]*distance, antenna2[1]+dir[1]*distance)
                    if antenoid[0] >= 0 and antenoid[1] >= 0 and antenoid[0] <= max_x-1 and antenoid[1] <= max_y-1:
                        antenoids.add(antenoid)
                    else:
                        break
                    distance+=1
    #check_antenna(data, antenoids)
    return len(antenoids)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
