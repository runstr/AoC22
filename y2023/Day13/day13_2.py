import pathlib
from copy import copy

from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
def check_reflection(this_row):

    for i in range(0, len(this_row)-1):
        left_add = 0
        right_add = 1
        reflection = True
        while True:
            if i+right_add >= len(this_row) or i-left_add < 0:
                break
            if this_row[i+right_add] != this_row[i-left_add]:
                reflection = False
                break
            right_add+=1
            left_add+=1
        if reflection:
            return i+1



def get_my_answer():
    maps = load_data(filepath, example=True).split("\n\n")
    total_sum = 0
    for this_map in maps:
        rows = this_map.split("\n")
        columns = [""]*len(rows[0])
        found=False
        for y in range(0, len(rows)):
            for x in range(0, len(columns)):
                new_rows = copy(rows)
                if rows[y][x] == ".":
                    new_row = rows[y][:x]+"#"+rows[y][x+1:]
                    new_rows[y]=new_row
                elif rows[y][x] == "#":
                    new_row = rows[y][:x]+"."+rows[y][x+1:]
                    new_rows[y] = new_row
                for row in new_rows:
                    for i, letter in enumerate(row):
                        columns[i] += letter
                row_reflection = check_reflection(new_rows)
                column_reflection = check_reflection(columns)
                if row_reflection is not None:
                    total_sum+=row_reflection*100
                    found = True
                    break
                if column_reflection is not None:
                    total_sum += column_reflection
                    found = True
                    break
                if row_reflection and column_reflection:
                    print("found both")
                if row_reflection is None and column_reflection is None:
                    print("found None")

            if found:
                break

    return total_sum


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2023)
