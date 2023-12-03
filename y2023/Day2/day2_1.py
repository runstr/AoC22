import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
max_cubes = {"red": 12, "green": 13, "blue": 14}

def get_my_answer():
    all_data = load_data_as_lines(filepath, example=False)
    all_game_date = {}
    for line in all_data:
        single_game_data = {"red": 0, "green": 0, "blue": 0}
        game, cubes = line.split(": ")
        game_int = int(game[5:])
        sets = cubes.split("; ")
        for _set in sets:
            for temp in _set.split(", "):
                digit, color = temp.split(" ")
                if int(digit) >single_game_data[color]:
                    single_game_data[color]= int(digit)
        all_game_date[game_int] = single_game_data
    my_answer = 0
    for game, data in all_game_date.items():
        if data["red"] <= max_cubes["red"] and data["blue"] <= max_cubes["blue"] and data["green"] <= max_cubes["green"]:
            my_answer+=game
    return my_answer


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
