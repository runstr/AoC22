import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def get_my_answer():
    current_directory="/"
    file_size = {}
    data = load_data_as_lines(filepath, example=False)
    for command in data:
        if command[0:4] == "$ cd":
            if command[-1] == "/":
                current_directory = "/"
            elif command.split(" ")[-1] == "..":
                current_directory = "/".join(current_directory.split("/")[0:-1])
            else:
                current_directory+=("/"+command.split(" ")[-1])
            print(current_directory)
        elif command.split(" ")[0].isdigit():
            try:
                file_size[current_directory] += int(command.split(" ")[0])
            except KeyError:
                file_size[current_directory] = int(command.split(" ")[0])
    new_total_size = {}
    for key, value in file_size.items():
        total_size = value
        for key2, value2 in file_size.items():
            if key2[0:len(key)+1] == key+"/":
                total_size+=value2
        new_total_size[key] = total_size
    total_sum = 0
    for key, value in new_total_size.items():
        if value <= 100000:
            total_sum += value
    return total_sum


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
