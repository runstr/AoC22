import pathlib
from copy import copy
import math
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def find_rx_signals(rx_start, modules):
    all_rx_paths = []
    return all_rx_paths



def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    modules = {}
    for line in data:
        module, outputs = line.split(" -> ")
        if module == "broadcaster":
            broadcast = outputs.split(", ")
            continue
        else:
            module_type = module[0]
            module = module[1:]
        if module_type == "%":
            state =0
        elif module_type == "&":
            state = {}
        else:
            raise Exception("Wrong type")
        outputs = outputs.split(", ")
        modules[module] = [module_type, outputs, state]
    end_nodes = set()
    for key, value in modules.items():
        for output in value[1]:
            if output in modules:
                if modules[output][0] == "&":
                    modules[output][2][key] = 0
            else:
                end_nodes.add(output)
                rx_start = key
    rx_paths = list(modules[rx_start][2].keys())
    num_signals = {0: 0, 1: 0}
    cycles = {key: [0] for key in rx_paths}
    for i in range(1, 10000):
        num_signals[0] += 1
        signals = [("broadcast", destination, 0) for destination in broadcast]
        while signals:
            source, destination, signal = signals.pop(0)
            if source in rx_paths:
                if all(list(modules[list(modules[source][2].keys())[0]][2].values())):
                    if i - cycles[source][-1] != 0:
                        cycles[source].append(i - cycles[source][-1])
            if destination in rx_paths:
                if all(list(modules[list(modules[destination][2].keys())[0]][2].values())):
                    cycles[destination].append(i - cycles[destination][-1])
            num_signals[signal] += 1
            if destination in end_nodes:
                continue
            if modules[destination][0] == "%":
                if signal == 1:
                    continue
                new_signal = not modules[destination][2]
                modules[destination][2] = new_signal
                for new_dest in modules[destination][1]:
                    signals.append((destination, new_dest, new_signal))
            elif modules[destination][0] == "&":
                modules[destination][2][source] = signal
                new_signal = not all(modules[destination][2].values())
                for new_dest in modules[destination][1]:
                    signals.append((destination, new_dest, new_signal))
    for key, value in cycles.items():
        print(key, value)
    return math.lcm(*[val[-1] for key, val in cycles.items()])


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
