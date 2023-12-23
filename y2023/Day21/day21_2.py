import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
from sympy.solvers import solve
from sympy import symbols, Eq

def get_neigbours(point, max_x, max_y, map_points):
    new_points = set()
    for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        new_point = (point[0] + dx, point[1] + dy)
        if new_point[0] < 0:
            new_x = (max_x-1)-abs(new_point[0]+1) % (max_x)
        elif new_point[0] >= max_x:
            new_x = new_point[0] % max_x
        else:
            new_x = new_point[0]
        if new_point[1] < 0:
            new_y = (max_y-1)-abs(new_point[1]+1) % (max_y)
        elif new_point[1] >= max_y:
            new_y = new_point[1] % max_y
        else:
            new_y = new_point[1]

        if map_points[(new_x, new_y)] != "#":
            new_points.add(new_point)
    return new_points

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    max_x = len(data)
    max_y = len(data[0])
    print(max_x, max_y)
    map_points = {}
    for y, line in enumerate(data):
        for x, letter in enumerate(line):
            if letter == "S":
                start_point = (x, y)
            map_points[(x, y)] = letter
    max_steps = start_point[0]+2*max_x+2
    travel_points = {start_point}
    print_points = [start_point[0], start_point[0]+max_x, start_point[0]+2*max_x]
    values = []
    for step in range(1, max_steps):
        new_points = set()
        for point in travel_points:
            neigbours = get_neigbours(point, max_x,  max_y, map_points)
            new_points |= neigbours
        travel_points = new_points
        possibilites = len(travel_points)
        if step in print_points:
            print(f"Step: {step}, possibilities: {possibilites}",)
            values.append((step, possibilites))
    x_value = 26501365
    final_result = quadratic_formula_given_poinst(values, x_value)

    return final_result[0]

def quadratic_formula_given_poinst(points, x_value):
    """ solve equation ax**2 +b*x + c = y. First get coeficients: then use x_value to return teh correct y_value"""
    a, b, c, y = symbols('a b c, y')
    eq1 = Eq(a * points[0][0] ** 2 + b * points[0][0] + c, points[0][1])
    eq2 = Eq(a * points[1][0] ** 2 + b * points[1][0] + c, points[1][1])
    eq3 = Eq(a * points[2][0] ** 2 + b * points[2][0] + c, points[2][1])
    result = solve([eq1, eq2, eq3], a, b, c)
    eq4 = Eq(result[a] * x_value ** 2 + result[b] * x_value + result[c], y)
    final_result = solve(eq4, y)
    return final_result

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
