import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

NUMBER_OF_GALAXIES = 10

def get_empty(index, empty):
    empty_lines = 0
    for empty_index in empty:
        if empty_index < index:
            empty_lines += 1
    return empty_lines


def get_my_answer():
    global NUMBER_OF_GALAXIES
    data = load_data_as_lines(filepath, example=True)
    empty_rows = []
    empty_columns = []
    x_max = len(data[0])
    for y, line in enumerate(data):
        if "#" not in line:
            empty_rows.append(y)

    for x in range(0, x_max):
        column = [dat[x] for dat in data]
        if "#" not in column:
            empty_columns.append(x)
    galaxies = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "#":
                empty_x = get_empty(x, empty_columns)
                empty_y = get_empty(y, empty_rows)
                galaxies.append((x+empty_x*NUMBER_OF_GALAXIES,y+empty_y*NUMBER_OF_GALAXIES))
    used_galaxies = []
    total_lengths = []
    for galaxy in galaxies:
        used_galaxies.append(galaxy)
        for galaxy2 in galaxies:
            if galaxy2 not in used_galaxies:
                total_lengths.append(abs(galaxy[0]-galaxy2[0])+abs(galaxy[1]-galaxy2[1]))



    return sum(total_lengths)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)


