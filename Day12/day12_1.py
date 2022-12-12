import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, load_data_as_chars, timeexecution
from aocd import submit
from queue import Queue
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    example = False
    data = load_data_as_chars(filepath, example=example)
    if example:
        startpoint = (0, 0)
        endpoint = (5, 2)
        data[2][5] = "z"
        data[0][0] = "a"
    else:
        startpoint = (0, 20)
        endpoint = (138, 20)
        data[20][138] = "z"
        data[20][0] = "a"
    startpoints = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x]=='a':
                startpoints.append((x,y))
    print(startpoints)
    adjacent = {}
    for y in range(0, len(data)):
        for x in range(0, len(data[0])):
            point = (x, y)
            adjacent_points=[]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if abs(dy) == 1 and abs(dx) == 1 or (dy == 0 and dx == 0):
                        continue
                    if x+dx<0 or x+dx >= len(data[0]) or y+dy < 0 or y+dy >= len(data):
                        continue
                    if ord(data[y+dy][x+dx]) <= ord(data[y][x])+1:
                        adjacent_points.append((x+dx, y+dy))
            adjacent[point] = adjacent_points
    lengths=dict()
    for startpoint in startpoints:
        visited = set()
        queue = Queue()
        queue.put(startpoint)
        visited.add(startpoint)
        parent = dict()
        parent[startpoint] =None
        path_found = False
        # loop until the queue is empty
        while not queue.empty():
            # pop the front node of the queue and add it to bfs_traversal

            current_node = queue.get()
            if current_node == endpoint:
                path_found = True
                break
            for neighbour_node in adjacent[current_node]:
                if neighbour_node not in visited:
                    queue.put(neighbour_node)
                    parent[neighbour_node] = current_node
                    visited.add(neighbour_node)
        path = []
        if path_found:
            target_node = endpoint
            path.append(target_node)
            while parent[target_node] is not None:
                path.append(parent[target_node])
                target_node = parent[target_node]
            path.reverse()
        lengths[startpoint] = len(path)-1
    shortest = 22222222
    for value in lengths.values():
        if value==-1:
            continue
        if value<shortest:
            shortest=value
    return shortest


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
