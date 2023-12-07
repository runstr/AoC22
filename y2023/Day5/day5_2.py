import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
import math
import time
def translate_source_to_dest(seed_ranges, transform):
    new_splits = seed_ranges
    new_destinations = []
    for destination_start, source_start, ranges in transform:
        old_splits = new_splits
        new_splits = []
        for seed_range in old_splits:
            new_dest, new_split = compare_ranges(seed_range,
                                             (source_start, ranges),
                                             (destination_start, ranges) )
            if new_dest:
                new_destinations.append(new_dest)
            if new_split:
                new_splits += new_split
    new_destinations += new_splits
    return new_destinations

def compare_ranges(seed_ranges, source_ranges, destination_ranges):
    seed_start, seed_end, seed_range = seed_ranges[0], seed_ranges[0]+seed_ranges[1], seed_ranges[1]
    source_start, source_end, source_range = source_ranges[0], source_ranges[0] + source_ranges[1], source_ranges[1]
    destination_start, destination_end, destination_range = destination_ranges[0], destination_ranges[0] + destination_ranges[1], destination_ranges[1]
    if seed_end > source_start and seed_start < source_end:
        if seed_start < source_start and seed_end > source_end:
            retval = destination_ranges, [(seed_start, source_start-seed_start), (source_end, seed_end-source_end)]
            return retval
        elif seed_start >= source_start and seed_end <= source_end:
            retval = (destination_start + seed_start-source_start, seed_range), []
            return retval
        elif seed_start >= source_start and seed_end >= source_end:
            new_range = seed_range - (seed_end - source_end)
            retval = (destination_start+source_range-new_range, new_range), [(source_end, seed_range - new_range)]
            return retval
        elif seed_start <= source_start and seed_end <= source_end:
            new_range = seed_end-source_start
            retval = (destination_start, new_range), [(seed_start, seed_range-new_range)]
            return retval
    else:
        return (), [seed_ranges]

def get_my_answer():
    data = load_data(filepath, example=False)
    data = data.split("\n\n")
    seeds = list(map(int, data[0].split(" ")[1:]))
    new_data = []
    for transform in data[1:]:
        new_transform = []
        for line in transform.split("\n")[1:]:
            new_transform.append(tuple(map(int, line.split(" "))))
        new_data.append(new_transform)
    source_range = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    for transform in new_data:
        source_range = (translate_source_to_dest(source_range, transform))

    min_val = math.inf
    for source in source_range:
        if source[0]<min_val:
            min_val = source[0]
    return min_val

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
