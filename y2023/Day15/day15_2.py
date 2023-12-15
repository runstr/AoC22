import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def hash_alogrithm(hash):
    this_sum = 0
    for letter in hash:
        this_sum += ord(letter)
        this_sum *= 17
        this_sum = this_sum % 256
    return this_sum

def get_my_answer():
    data = load_data(filepath, example=False)
    my_map: dict(int, list) = {i: [] for i in range(256)}
    focal_lengths = {}
    index = 0
    for line in data.split(","):
        dash_index = line.find("-")

        if dash_index < 0:
            eq_index = line.find("=")
            label, focal_length = line.split("=")
        else:
            label, focal_length = line.split("-")
        hash_number = hash_alogrithm(label)
        if dash_index >= 0:
            if label in my_map[hash_number]:
                my_map[hash_number].remove(label)
                focal_lengths[label] = 0
        else:
            if label not in my_map[hash_number]:
                my_map[hash_number].append(label)
            focal_lengths[label] = int(focal_length)
    focusing_power = 0

    for key, value in my_map.items():
        for i, val in enumerate(value):
            focusing_power += ((int(key)+1)*(i+1)*focal_lengths[val])
            print(key, val, focal_lengths[val])




    return focusing_power


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
