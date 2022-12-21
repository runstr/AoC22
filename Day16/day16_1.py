import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
from copy import deepcopy

filepath = pathlib.Path(__file__).parent.resolve()


def bfs(start_path, end_path, all_paths):
    visited = set()
    queue = []
    queue.append(start_path)
    visited.add(start_path)
    parent = dict()
    parent[start_path] = None
    # loop until the queue is empty
    while queue:
        current_node = queue.pop(0)
        if current_node == end_path:
            break
        for neighbour_node in all_paths[current_node]:
            if neighbour_node not in visited:
                queue.append(neighbour_node)
                parent[neighbour_node] = current_node
                visited.add(neighbour_node)
    path = []
    target_node = end_path
    path.append(target_node)
    while parent[target_node] is not None:
        path.append(parent[target_node])
        target_node = parent[target_node]
    path.reverse()
    return (path, len(path)-1)


def get_fastest_paths(flow_rate, all_paths):
    non_zero_flow_rates = []
    for key, value in flow_rate.items():
        if value > 0 or key == "AA":
            non_zero_flow_rates.append(key)
    shortest_paths = {}
    for path1 in non_zero_flow_rates:
        for path2 in non_zero_flow_rates:
            if path1 == path2:
                continue
            shortest_paths[path1+"-"+path2] = bfs(path1, path2, all_paths)
    return shortest_paths


def move_person(cave, shortest_paths, flow_rates, total_pressure, current_pressure, time_left, all_paths, current_path, open_valves):
    for keys in shortest_paths.keys():
        if keys[:2] != cave:
            continue
        next_cave = keys[-2:]
        if open_valves[next_cave]:
            continue
        # Moving person
        this_open_valves = deepcopy(open_valves)
        this_path = current_path
        this_total_pressure = total_pressure
        this_current_pressure = current_pressure
        this_time_left = time_left

        time_taken = shortest_paths[keys][1]
        if time_taken >= time_left:
            this_pressure_released = current_pressure * time_left
            this_total_pressure += this_pressure_released
            all_paths[this_path] = this_total_pressure
            continue
        this_pressure_released = current_pressure * time_taken
        this_total_pressure += this_pressure_released
        this_time_left-=time_taken
        all_paths[this_path] = this_total_pressure + this_current_pressure * this_time_left
        # opening valve
        this_total_pressure += current_pressure
        this_current_pressure += flow_rates[next_cave]
        this_open_valves[next_cave] = True

        this_path += ("-"+next_cave)
        this_time_left -= 1
        move_person(next_cave, shortest_paths, flow_rates, this_total_pressure, this_current_pressure, this_time_left, all_paths, this_path, this_open_valves)
    return


def get_my_answer():
    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
    data = load_data_as_lines(filepath, example=True)
    all_paths = {}
    flow_rates = {}
    open_valves = {}
    for line in data:
        valve = line.split("Valve ")[1][:2]
        open_valves[valve] = False
        flow_rate = line.split("flow rate=")[1].split(";")[0]
        flow_rates[valve] = int(flow_rate)
        if "valves" in line:
            lead_to = line.split("valves ")[1].split(", ")
        else:
            lead_to = line.split("valve ")[1].split(",")
        all_paths[valve] = lead_to
    shortest_paths = get_fastest_paths(flow_rates, all_paths)
    current_path = "AA"
    cave = "AA"
    total_pressure = 0
    current_pressure = 0
    time_left = 30
    total_paths = {}
    move_person(cave, shortest_paths, flow_rates, total_pressure, current_pressure, time_left, total_paths, current_path, open_valves)
    max_value = max(list(total_paths.values()))
    for key, value in total_paths.items():
        if value == max_value:
            print(key, value)
            print(len(total_paths))
    return None


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
