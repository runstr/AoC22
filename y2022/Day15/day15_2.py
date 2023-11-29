import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
import re
MAX_VALUE = 4000000

def calculate_manhatten_distance(p1, p2):
     return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def combine_ranges(ranges):
    left_side = 0
    right_side = 0
    for i in range(len(ranges)):
        if (ranges[i][0]<0 and ranges[i][1]<0) or (ranges[i][0]>MAX_VALUE and ranges[i][1]>MAX_VALUE):
            continue
        if ranges[i][0] < 0:
            ranges[i] = (0, ranges[i][1])
        if ranges[i][1] > MAX_VALUE:
            ranges[i] = (ranges[i][0],MAX_VALUE)
        left_value_in_range = check_if_in_range(ranges[i][0], left_side, right_side)
        right_value_in_range = check_if_in_range(ranges[i][1], left_side, right_side)
        if left_value_in_range and right_value_in_range:
            continue
        if not left_value_in_range:
            return True, ranges[i][0]
        right_side = ranges[i][1]
    return False, -1


def check_if_in_range(value, min_x, max_x):
    if value >= min_x and value <= max_x:
        return True
    else:
        return False





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
    for test_line in range(4000000, -1, -1):
        ranges = []
        for scanner in scanners:
            distance = calculate_manhatten_distance(scanner, closets_devices[scanner])
            dy = abs(scanner[1]-test_line)
            distance_left = distance-dy
            if distance_left >= 0:
                left_side = scanner[0] - distance_left
                right_side = scanner[0] + distance_left
                ranges.append((left_side, right_side))
        ranges = sorted(ranges)
        found_value, value = combine_ranges(ranges)
        if found_value:
            break
    print(test_line, value-1)

    return (value-1)*4_000_000+test_line


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
