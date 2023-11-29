import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
NEXT_ROCK_ORDER = {"-": "+", "+": "L", "L": "I", "I": "S", "S": "-"}
ROCKS = {"-": [(2, 4), (3, 4), (4, 4), (5, 4)],
         "+": [(2, 5), (3, 5), (4, 5), (3, 4), (3, 6)],
         "L": [(2, 4), (3, 4), (4, 4), (4, 5), (4, 6)],
         "I": [(2, 4), (2, 5), (2, 6), (2, 7)],
         "S": [(2, 4), (3, 4), (2, 5), (3, 5)]}

class Cave:
    def __init__(self, example):
        self.heights = {0: {0}, 1: {0}, 2: {0}, 3: {0}, 4: {0}, 5: {0}, 6: {0}}
        self.max_heights = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.original_jets = load_data(filepath, example=example)
        self.current_jets = self.original_jets
        self.next_rock= "-"
        self.current_rock = []

    def add_rock(self):
        rock = ROCKS[self.next_rock]
        self.next_rock = NEXT_ROCK_ORDER[self.next_rock]
        max_height = max(self.max_heights.values())
        new_rock = []
        for i in range(len(rock)):
            new_rock.append((rock[i][0], rock[i][1]+max_height))
        self.current_rock = new_rock

    def move_rock(self):
        try:
            movement = self.current_jets[0]
        except IndexError:
            self.current_jets = self.original_jets
            movement = self.current_jets[0]
        self.current_jets = self.current_jets[1:]
        if movement == "<":
            self.move_left()
        else:
            self.move_right()

        return self.move_down()

    def move_left(self):
        for coordinate in self.current_rock:
            x_coordinate = coordinate[0]
            y_coordinate = coordinate[1]
            if x_coordinate - 1 < 0:
                return False
            left_heights = self.heights[x_coordinate-1]
            if y_coordinate in left_heights:
                return False
        for i in range(len(self.current_rock)):
            self.current_rock[i] = (self.current_rock[i][0]-1, self.current_rock[i][1])
        return True

    def move_right(self):
        for coordinate in self.current_rock:
            x_coordinate = coordinate[0]
            y_coordinate = coordinate[1]
            if x_coordinate + 1 > 6:
                return False
            right_heights = self.heights[x_coordinate+1]
            if y_coordinate in right_heights:
                return False
        for i in range(len(self.current_rock)):
            self.current_rock[i] = (self.current_rock[i][0]+1, self.current_rock[i][1])
        pass

    def move_down(self):
        for coordinate in self.current_rock:
            x_coordinate = coordinate[0]
            y_coordinate = coordinate[1]
            heights = self.heights[x_coordinate]
            if y_coordinate-1 in heights:
                return False
        for i in range(len(self.current_rock)):
            self.current_rock[i] = (self.current_rock[i][0], self.current_rock[i][1]-1)
        return True

    def update_heights(self):
        for coordinate in self.current_rock:
            x_coordinate = coordinate[0]
            y_coordinate = coordinate[1]
            self.heights[x_coordinate].add(y_coordinate)
            self.max_heights[x_coordinate] = max(self.max_heights[x_coordinate], y_coordinate)

    def iterate(self, num_rocks):
        self.add_rock()
        i = 0
        while i < num_rocks:
            #self.print_cave()
            if self.move_rock():
                continue
            self.update_heights()
            self.add_rock()
            i += 1

    def print_heights(self):
        print(self.heights)

    def get_max_height(self):
        return max(self.max_heights.values())

    def print_cave(self):
        height = self.get_max_height()+6
        while height > 0:
            print("| ", end="")
            for i in range(len(self.heights.keys())):
                if height in self.heights[i]:
                    print("# ", end="")
                elif (i, height) in self.current_rock:
                    print("@ ", end="")
                else:
                    print(". ", end="")
            print("|")
            height -= 1
        print("+ - - - - - - - +")


def get_my_answer():
    cave = Cave(example=False)
    cave.iterate(2022)
    max_height = cave.get_max_height()
    return max_height


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
