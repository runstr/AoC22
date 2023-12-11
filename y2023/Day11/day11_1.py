import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=True)
    empty_rows = []
    empty_columns = []
    new_data = []
    x_max = len(data[0])
    for y, line in enumerate(data):
        if "#" not in line:
            new_data.append(".........."*x_max)
        new_data.append(line)
    y_max = len(new_data)
    newest_data = ["" for _ in range(y_max)]
    for y in range(0, x_max):
        column = [data[y] for data in new_data]
        if "#" not in column:
            for i in range(len(column)):
                newest_data[i] += ".........."
        for i in range(len(column)):
            newest_data[i] += column[i]
    galaxies = []
    for y in range(len(newest_data)):
        for x in range(len(newest_data[0])):
            if newest_data[y][x] == "#":
                galaxies.append((x, y))
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
        submit(my_answer, part="a", day=this_day, year=2023)


