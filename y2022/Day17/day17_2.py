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
        self.example = example
        self.heights = {0: {0}, 1: {0}, 2: {0}, 3: {0}, 4: {0}, 5: {0}, 6: {0}}
        self.max_heights = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.min_height = 0
        self.original_jets = load_data(filepath, example=example)
        self.current_jets = self.original_jets
        self.next_rock = "-"
        self.this_rock = "-"
        self.index = 0
        self.current_rock = []
        self.last_removed = 0
        self.same_index = []
        self.same_rocks = []
        self.same_heights = []
        self.rock_number = 0

    def add_rock(self):
        rock = ROCKS[self.next_rock]
        self.rock_number+=1
        self.this_rock = self.next_rock
        self.next_rock = NEXT_ROCK_ORDER[self.next_rock]
        max_height = max(self.max_heights.values())
        new_rock = []
        for i in range(len(rock)):
            new_rock.append((rock[i][0], rock[i][1]+max_height))
        self.current_rock = new_rock

    def move_rock(self):
        try:
            movement = self.current_jets[0]
            self.index += 1
        except IndexError:
            self.current_jets = self.original_jets
            self.index = 0
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

    def find_repetitive(self):
        self.add_rock()
        while True:
            if self.move_rock():
                continue
            self.update_heights()
            self.add_rock()
            if self.check_plus_rock() and self.check_flat_line():
                if self.index in self.same_index:
                    self.same_index.append(self.index)
                    self.same_rocks.append(self.rock_number)
                    self.same_heights.append(self.get_max_height())
                    break
                else:
                    self.same_index.append(self.index)
                    self.same_rocks.append(self.rock_number)
                    self.same_heights.append(self.get_max_height())
        repetitive_index = self.same_index[-1]
        start_index = self.same_index.index(self.same_index[-1])
        repetitive_height = self.same_heights[-1] - self.same_heights[start_index]
        repetitive_rocks = self.same_rocks[-1] - self.same_rocks[start_index]
        start_rock = self.same_rocks[-1]
        start_height = self.same_heights[-1]
        self.reset_cave()
        return repetitive_height, repetitive_rocks, start_height, start_rock, repetitive_index

    def get_first_x_heights(self, repetitive_height, repetitive_rocks, start_height, start_rock, x):
        rocks = [start_rock]
        heights = [start_height]
        for i in range(x):
            rocks.append(rocks[i]+repetitive_rocks)
            heights.append(heights[i]+repetitive_height)
        return rocks, heights

    def reset_cave(self):
        self.heights = {0: {0}, 1: {0}, 2: {0}, 3: {0}, 4: {0}, 5: {0}, 6: {0}}
        self.max_heights = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.min_height = 0
        self.original_jets = self.original_jets
        self.current_jets = self.original_jets
        self.next_rock = "-"
        self.this_rock = "-"
        self.index = 0
        self.current_rock = []
        self.last_removed = 0
        self.same_index = []
        self.same_rocks = []
        self.same_heights = []
        self.rock_number = 0

    def iterate(self, num_rocks):
        self.add_rock()
        while self.rock_number <= num_rocks:
            if self.move_rock():
                continue
            self.update_heights()
            self.add_rock()
            self.remove_unnecessary_heights()

    def print_heights(self):
        print(self.heights)

    def check_flat_line(self):
        max_values = list(self.max_heights.values())
        for value in max_values:
            if value != max_values[0]:
                return False
        return True

    def check_plus_rock(self):
        if self.this_rock == "+":
            return True
        return False

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
            if height < self.min_height:
                break
        print("+ - - - - - - - +")

    def remove_unnecessary_heights(self):
        min_height = min(self.max_heights.values())
        self.min_height = min_height
        if min_height == self.last_removed:
            return
        for heights in self.heights.values():
            heights_to_remove = []
            for height in heights:
                if height < min_height:
                    heights_to_remove.append(height)
            for height in heights_to_remove:
                heights.remove(height)
        self.last_removed = min_height

    def update_jets(self, index):
        self.current_jets = self.original_jets[index:]

    def update_start_block(self, rock):
        self.next_rock = rock
        self.this_rock = rock

    def check_repetitive(self, heights, rocks):
        self.add_rock()
        rock_index = 0
        while True:
            if self.move_rock():
                continue
            self.update_heights()
            self.add_rock()
            if self.rock_number == rocks[rock_index]:
                max_height = self.get_max_height()
                supposed_height = heights[rock_index]
                if supposed_height != max_height:
                    raise Exception("Something is wrong")
                rock_index+=1
            if rock_index>= len(heights):
                break

            self.remove_unnecessary_heights()
        self.reset_cave()


def get_my_answer():
    cave = Cave(example=False)
    repetitive_height, repetitive_rocks, start_height, start_rock, start_index = cave.find_repetitive()
    print(repetitive_height, repetitive_rocks, start_height, start_rock)
    rocks, heights=cave.get_first_x_heights(repetitive_height, repetitive_rocks, start_height, start_rock, 100)
    print(rocks, "\n", heights)
    total_rocks = 1_000_000_000_000
    number_of_repititions = (total_rocks-start_rock)//repetitive_rocks
    print(number_of_repititions)
    total_height = start_height+number_of_repititions*repetitive_height
    print(total_height)
    rocks_left = total_rocks-number_of_repititions*repetitive_rocks-start_rock
    print(rocks_left)
    # cave.check_repetitive(heights, rocks)
    # cave = Cave(example=False)
    cave.update_jets(start_index+1)
    cave.update_start_block("+")
    cave.iterate(rocks_left+1)

    max_height = cave.get_max_height()
    return max_height + total_height

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
