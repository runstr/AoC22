import pathlib
from copy import copy

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
    rx_paths = find_rx_signals(rx_start, modules)
    num_signals = {0: 0, 1: 0}
    rx_low_signals = 0
    signals = [("broadcast", destination, 0) for destination in broadcast]
    total_signals = []
    for i in range(1, 10000):
        num_signals[0] += 1
        signals = [("broadcast", destination, 0) for destination in broadcast]
        rx_low_signals = 0
        bit_signals = []
        rx_signals = []
        while signals:
            source, destination, signal = signals.pop(0)
            if source != "broadcast":
                bit_signals.append((source, modules[source][0], int(signal)))
            num_signals[signal]+=1
            if destination in end_nodes:
                if destination == "rx":
                    rx_signals.append(signal)
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
                pass
            else:
                raise Exception("Wrong type")
        print([list(modules[rx_path][2].values()) for rx_path in rx_paths])
        total_value = 0
        for value in modules.values():
            if value[0] == "&":
                total_value += sum(value[2].values())
            else:
                total_value += value[2]
        total_signals.append(total_value)

        if total_value == 0:
            print(f"cycle after {i} iterations")
        if not i % 100000:
            print(i)
        if rx_low_signals == 1:
            print(f"iteration: {i}, rx_presses: {rx_low_signals}")
            break
    print(total_signals)
    return num_signals[0]*num_signals[1]


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
