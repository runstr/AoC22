import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution, load_data_as_chars
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = load_data_as_chars(filepath, example=False)
    regions = []
    visited = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (x, y) in visited:
                continue
            current_garden = data[y][x]
            next_points = [(x, y)]
            perimiter = 0
            area = 0
            while next_points:
                point = next_points.pop(0)
                if point in visited:
                    continue
                area+=1
                visited.add(point)
                for dirx, diry in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    new_point = (point[0]+dirx, point[1]+diry)
                    if new_point[0] < 0 or new_point[0] >= len(data[0]) or new_point[1] < 0 or new_point[1] >= len(data):
                        perimiter += 1
                        continue
                    if data[point[1]+diry][point[0]+dirx] == current_garden:
                        next_points.append(new_point)
                    else:
                        perimiter += 1
            regions.append((perimiter, area))
    total_sum = 0
    for perimiter, area in regions:
        total_sum += perimiter*area
    return total_sum



@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
