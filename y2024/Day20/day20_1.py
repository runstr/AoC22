import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    racetrack = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == ".":
                racetrack.add((x, y))
            elif data[y][x] == "S":
                racetrack.add((x, y))
                start_point = (x, y)
            elif data[y][x] == "E":
                racetrack.add((x, y))
                end_point = (x, y)
    race_map = {}
    next_points = [start_point]
    picoseconds = 0
    while next_points:
        point = next_points.pop(0)

        race_map[point] = picoseconds
        picoseconds+=1

        for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            new_point = (point[0]+dx, point[1]+dy)
            if new_point in racetrack and new_point not in race_map:
                next_points.append(new_point)
    minimum_saving = 100
    minimum_savings= {}
    for point, value in race_map.items():
        for dx, dy in [(2, 0), (-2, 0), (0, -2), (0, 2)]:
            new_point = (point[0]+dx, point[1]+dy)
            if new_point in racetrack:
                if race_map[new_point]-value >= minimum_saving+2:
                    minimum_savings[(point, new_point)] = race_map[new_point]-value - 2
    for key, value in minimum_savings.items():
        print(key, value)
    return len(minimum_savings)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
