import math
import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


class Rock:
    def __init__(self, number):
        self.id = number
        self.children: list[Rock] | None = []
        self.num_children = 0
        self.num_parents = 0
        self.parents: list[Rock] | None = []
        self.coordinates = []
        self.height = 0

    def __hash__(self):
        return self.coordinates

def get_connections(nodes, max_x, max_y):
    all_rocks = []
    rocks: dict[tuple[int, int], Rock | None] | None = {}
    for x in range(max_x+1):
        for y in range(max_y+1):
            rocks[(x, y)] = None

    for node in nodes:
        (x, y, z), (dx, dy, dz), number = node
        new_rock = Rock(number)
        if dz > 0 or dx == dy == dz == 0:
            if rocks[(x, y)] is None:
                new_rock.height = dz+1
                new_rock.coordinates = [(x, y)]
            else:
                old_rock = rocks[(x, y)]
                new_rock.height = old_rock.height + dz+1
                new_rock.coordinates = [(x, y)]
                old_rock.children.append(new_rock)
                old_rock.num_children += 1
                new_rock.parents.append(old_rock)
                new_rock.num_parents += 1
            rocks[(x, y)] = new_rock
        elif dx > 0:
            old_rocks = []
            max_height = 0
            for i in range(0, dx+1):
                old_rock = rocks[(x+i, y)]
                new_rock.coordinates.append((x+i, y))
                if old_rock is not None:
                    if old_rock.height > max_height:
                        max_height = old_rock.height
                    old_rocks.append(old_rock)
            new_rock.height = max_height+1
            for old_rock in old_rocks:
                if old_rock.height == max_height:
                    old_rock.children.append(new_rock)
                    old_rock.num_children += 1
                    new_rock.parents.append(old_rock)
                    new_rock.num_parents += 1
            for i in range(0, dx+1):
                rocks[(x+i, y)] = new_rock
        elif dy > 0:
            old_rocks = []
            max_height = 0
            for i in range(0, dy+1):
                old_rock = rocks[(x, y+i)]
                new_rock.coordinates.append((x, y+i))
                if old_rock is not None:
                    if old_rock.height > max_height:
                        max_height = old_rock.height
                    old_rocks.append(old_rock)
            new_rock.height = max_height+1
            for old_rock in old_rocks:
                if old_rock.height == max_height:
                    old_rock.children.append(new_rock)
                    old_rock.num_children += 1
                    new_rock.parents.append(old_rock)
                    new_rock.num_parents += 1
            for i in range(0, dy+1):
                rocks[(x, y+i)] = new_rock
        else:
            print("hi")
        all_rocks.append(new_rock)
    return rocks, all_rocks


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    new_nodes = []
    max_x, max_y = 0, 0
    min_x, min_y = math.inf, math.inf
    for i, line in enumerate(data):
        start_node, end_node = line.split("~")
        (x, y, z) = tuple(map(int, start_node.split(",")))
        if x<min_x:
            min_x=x
        if y<min_y:
            min_y=y
        (x2, y2, z2) = tuple(map(int, end_node.split(",")))
        if x2>max_x:
            max_x=x
        if y2>max_y:
            max_y=y
        (dx, dy, dz) = (x2-x, y2-y, z2-z)
        new_nodes.append(((x, y, z), (dx, dy, dz), i))
    new_nodes.sort(key=lambda coord: coord[0][2])
    rocks, all_rocks = get_connections(new_nodes, max_x, max_y)
    removable_rocks = 0
    for rock in all_rocks:
        if rock.num_children == 0:
            removable_rocks += 1
        else:
            removable = True
            for child in rock.children:
                if len(set([parent.id for parent in child.parents]))==1:
                    removable = False
                    break
            if removable:
                removable_rocks += 1
        print("coordinates: ", rock.coordinates, ", heigth: ", rock.height, ", children: ", rock.num_children, ", parents: ", rock.num_parents)

    return removable_rocks

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
