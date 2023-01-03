import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import re

filepath = pathlib.Path(__file__).parent.resolve()


def calculate_manhatten_distance(p1, p2):
     return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_all_distances(beacons, scanners):
    manhatten_distances = dict()
    for scanner in scanners:
        manhatten_distances[scanner] = dict()
        for beacon in beacons:
            distance = calculate_manhatten_distance(scanner, beacon)
            manhatten_distances[scanner][beacon] = distance
    return manhatten_distances


def get_my_answer():
    example = False
    data = load_data_as_lines(filepath, example=example)
    if example:
        test_line = 10
    else:
        test_line = 2000000
    closets_devices = {}
    beacons = []
    scanners = []
    for line in data:
        test = re.split(', |=|:', line)
        scanner = (int(test[1]), int(test[3]))
        beacon = (int(test[5]), int(test[7]))
        closets_devices[scanner] = beacon
        beacons.append(beacon)
        scanners.append(scanner)
    # Calculate manhatten distance

    no_beacons = set()
    for scanner in scanners:
        distance = calculate_manhatten_distance(scanner, closets_devices[scanner])
        dy = abs(scanner[1]-test_line)
        distance_left = distance-dy
        if distance_left >= 0:
            no_b_left = set(range(scanner[0] - distance_left, scanner[0]))
            no_b_right = set(range(scanner[0], scanner[0] + distance_left + 1))

            no_beacons = no_beacons | no_b_right | no_b_left
    for beacon in beacons:
        if beacon[0] in no_beacons and beacon[1]==test_line:
            no_beacons.remove(beacon[0])
    return len(no_beacons)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
