import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def expand_and_map_input(data):
    map = {}
    elves = {}
    # Expand data
    for y, line in enumerate(data):
        line = "."*1000+line+"."*1000
        data[y] = line
    data = ["." * len(data[0]) for _ in range(500)] + data + ["." * len(data[0]) for _ in range(500)]
    # Map data
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            map[(x, y)] = value
            if value == "#":
                elves[(x, y)] = ["N", "S", "W", "E"]
    return map, elves


def check_surroundings(elf, mapping):
    can_move = {"N":False, "S":False, "W": False, "E": False}
    if mapping[(elf[0], elf[1]-1)] == "." and mapping[(elf[0]-1, elf[1]-1)] == "." and mapping[(elf[0]+1, elf[1]-1)] == ".":
        can_move["N"] = True
    if mapping[(elf[0], elf[1]+1)] == "." and mapping[(elf[0]-1, elf[1]+1)] == "." and mapping[(elf[0]+1, elf[1]+1)] == ".":
        can_move["S"] = True
    if mapping[(elf[0]-1, elf[1]-1)] == "." and mapping[(elf[0]-1, elf[1]+1)] == "." and mapping[(elf[0]-1, elf[1])] == ".":
        can_move["W"] = True
    if mapping[(elf[0]+1, elf[1]-1)] == "." and mapping[(elf[0]+1, elf[1]+1)] == "." and mapping[(elf[0]+1, elf[1])] == ".":
        can_move["E"] = True
    return can_move


def get_proposition(elves, mapping):
    elf_posibilites = {}
    for elf in elves.keys():
        elf_posibilites[elf] = check_surroundings(elf, mapping)
    elf_proposition = {}
    for elf in elves.keys():
        elf_proposition_order = elves[elf]
        elf_proposition[elf] = None
        if all(elf_posibilites[elf].values()):
            elf_proposition[elf] = None
            elves[elf] = elves[elf][1:] + elves[elf][:1]
            continue
        for dir in elf_proposition_order:
            if elf_posibilites[elf][dir]:
                elf_proposition[elf] = dir
                break
        elves[elf] = elves[elf][1:] + elves[elf][:1]
    return elf_proposition


def move_elves(elf_propsitions):
    old_to_new = {}
    all_new = {}
    for elf, proposition in elf_propsitions.items():
        if proposition is None:
            dx, dy = 0, 0
        else:
            dx, dy = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}[proposition]
        new = (elf[0]+dx, elf[1]+dy)
        old_to_new[elf] = new
        try:
            all_new[new] += 1
        except KeyError:
            all_new[new] = 1
    not_moving_to = []
    for new, number in all_new.items():
        if number > 1:
            not_moving_to.append(new)
    for old, new in old_to_new.items():
        if new in not_moving_to:
            old_to_new[old] = old
    return old_to_new


def update_mapping(mapping, elves, old_to_new):
    new_elves = {}
    for elf, values in elves.items():
        new_elves[old_to_new[elf]] = values
        mapping[old_to_new[elf]] = "#"
        if elf != old_to_new[elf]:
            mapping[elf]="."
    return new_elves


def print_mapping(mapping):
    current_line = 0
    for coord, value in mapping.items():
        if coord[1] > current_line:
            print()
            current_line = coord[1]
        print(value, end="")


def number_of_elves(mapping):
    number_of_elves = 0
    for coord, value in mapping.items():
        if value=="#":
            number_of_elves+=1
    return number_of_elves


def check_moving(old_to_new):
    moving = False
    for key, value in old_to_new.items():
        if key != value:
            moving = True
            break
    return moving


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    mapping, elves = expand_and_map_input(data)
    round = 0
    while True:
        round += 1
        elf_propositions = get_proposition(elves, mapping)
        old_to_new = move_elves(elf_propositions)
        if not check_moving(old_to_new):
            break
        elves = update_mapping(mapping, elves, old_to_new)
    return round


def boundin_box(mapping):
    minx, miny, maxx, maxy = math.inf, math.inf, -math.inf, -math.inf
    for coordinates, value in mapping.items():
        if value == "#":
            minx = min(minx, coordinates[0])
            maxx = max(maxx, coordinates[0])
            miny = min(miny, coordinates[1])
            maxy = max(maxy, coordinates[1])
    return minx, maxx, miny, maxy


def count_open(mapping, minx, maxx, miny, maxy):
    open_areas = 0
    for coord, value in mapping.items():
        if value == "." and coord[0]>=minx and coord[0]<=maxx and coord[1]>=miny and coord[1]<=maxy:
            open_areas += 1
    return open_areas


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
