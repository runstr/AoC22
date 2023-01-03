import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
from copy import deepcopy
filepath = pathlib.Path(__file__).parent.resolve()


def decode_input(data):
    blueprints = []
    for line in data:
        ore = {}
        clay = {}
        obsidian = {}
        geode = {}
        costs = line[:-1].split(": ")[1].split(". ")[0:4]
        blueprint = {}
        for cost in costs:
            all_words = cost.split(" ")
            if all_words[1] == "ore":
                ore["ore"] = int(all_words[-2])
                blueprint["ore"] = ore
            elif all_words[1] == "clay":
                clay["ore"] = int(all_words[-2])
                blueprint["clay"] = clay
            elif all_words[1] == "obsidian":
                obsidian["ore"] = int(all_words[-5])
                obsidian["clay"] = int(all_words[-2])
                blueprint["obsidian"] = obsidian
            elif all_words[1] == "geode":
                geode["ore"] = int(all_words[-5])
                geode["obsidian"] = int(all_words[-2])
                blueprint["geodes"] = geode
        blueprints.append(blueprint)
    return blueprints


def get_possible_robots(blueprint, materials):
    possible_robots = {"ore": False, "clay": False, "obsidian": False, "geodes": False, "none": True}
    for key, value in blueprint.items():
        if key == "ore":
            possible_robots["ore"] = materials["ore"] >= blueprint[key]["ore"]
        elif key == "clay":
            possible_robots["clay"] = materials["ore"] >= blueprint[key]["ore"]
        elif key == "obsidian":
            possible_robots["obsidian"] = (materials["ore"] >= blueprint[key]["ore"] and materials["clay"] >= blueprint[key]["clay"])
        elif key == "geodes":
            possible_robots["geodes"] = (materials["ore"] >= blueprint[key]["ore"] and materials["obsidian"] >= blueprint[key]["obsidian"])
        else:
            raise Exception("Something went wrong")
    return possible_robots


def update_materials(materials, robots):
    for key, value in robots.items():
        materials[key] += value
    return materials


def check_possible_extra_geodes(minutes_left, current_geodes, geo_robots):
    max_geodes = current_geodes
    for i in range(1, minutes_left+1):
        max_geodes += geo_robots
        max_geodes += i
    return max_geodes


def update_with_max_robots(blueprint, robots, possible_robots):
    max_ore = max(blueprint["ore"]["ore"], blueprint["clay"]["ore"], blueprint["obsidian"]["ore"], blueprint["geodes"]["ore"])
    if robots["ore"] >= max_ore:
        possible_robots["ore"] = False
    if robots["clay"] >= blueprint["obsidian"]["clay"]:
        possible_robots["clay"] = False
    if robots["obsidian"] >= blueprint["geodes"]["obsidian"]:
        possible_robots["obsidian"] = False
    return possible_robots


def use_materials(costs, materials):
    for key, value in costs.items():
        materials[key] -= value
    return materials


def update_with_last_possible(possible, last_possible):
    for key, value in last_possible:
        if value and key != "none":
            possible[key] = False
    return possible


def dfs(blueprint, robots, minute, materials, max_geodes, max_time, robot_produced,  last_possible=None):
    minute += 1
    # Get all possible robots with given materials
    possible_robots = get_possible_robots(blueprint, materials)

    # Update materials
    materials = update_materials(materials, robots)

    if minute == max_time:
        max_geodes[0] = max(max_geodes[0], materials["geodes"])
        return

    if minute == max_time-1:
        if possible_robots["geodes"]:
            max_geodes[0] = max(max_geodes[0], materials["geodes"] + robots["geodes"]+1)
        else:
            max_geodes[0] = max(max_geodes[0], materials["geodes"] + robots["geodes"])
        return
    if minute == max_time-2:
        possible_robots["clay"] = False

    if minute >= 20:
        possible_robots["clay"] = False
        possible_robots["ore"] = False

    if possible_robots["geodes"]:
        possible_robots["none"] = False

    # Drop production of robot if robots are more than max needed
    possible_robots = update_with_max_robots(blueprint, robots, possible_robots)

    # if last possible was not produced, they should not be produced this round either
    if last_possible:
        possible_robots = update_with_last_possible(possible_robots, last_possible)


    # Prune if it is not possible to produce more robots than already max
    if check_possible_extra_geodes(minutes_left=max_time-minute, current_geodes=materials["geodes"],
                                   geo_robots=robots["geodes"]) <= max_geodes[0]:
        return

    for key, value in possible_robots.items():
        if value:
            new_robots = {"ore": robots["ore"], "clay": robots["clay"], "obsidian": robots["obsidian"], "geodes": robots["geodes"]}
            new_materials = {"ore": materials["ore"], "clay": materials["clay"], "obsidian": materials["obsidian"], "geodes": materials["geodes"]}
            if key == "none":
                dfs(blueprint, new_robots, minute, new_materials, max_geodes, max_time, key, last_possible)
            else:
                new_robots[key] += 1
                new_materials = use_materials(blueprint[key], new_materials)
                dfs(blueprint, new_robots, minute, new_materials, max_geodes, max_time, key)


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    blueprints = decode_input(data)
    total = 1
    max_time = 32
    for i, blueprint in enumerate(blueprints):
        if i > 2:
            break
        max_geodes = [0]
        dfs(blueprint=blueprint,
            robots={"ore": 1, "clay": 0, "obsidian": 0, "geodes": 0},
            minute=0,
            materials={"ore": 0, "clay": 0, "obsidian": 0, "geodes": 0},
            max_geodes=max_geodes,
            max_time=max_time,
            robot_produced="none")
        print(i+1, ": ", max_geodes[0])
        total *= (max_geodes[0])
    return total


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
