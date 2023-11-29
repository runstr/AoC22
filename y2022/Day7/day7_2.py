import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    current_directory="/"
    file_size = {"/": 0}
    data = load_data_as_lines(filepath, example=False)
    for command in data:
        command_list = command.split()
        if command_list[1] == "cd":
            if command_list[-1] == "/":
                current_directory = "/"
            elif command_list[-1] == "..":
                current_directory = "/".join(current_directory.split("/")[0:-1])
            else:
                current_directory+=("/"+command_list[-1])
        elif command_list[0] == "dir":
            file_size[current_directory+"/"+command_list[1]] = 0
        elif command_list[0].isdigit():
            file_size[current_directory] += int(command_list[0])
    new_total_size = {}
    for key, value in file_size.items():
        total_size = value
        for key2, value2 in file_size.items():
            if key2[0:len(key)+1] == key+"/":
                total_size+=value2
        new_total_size[key] = total_size
    space_to_delete = new_total_size["/"]-(40000000)
    min_value = 999999999999
    for key,  value in new_total_size.items():
        if value>=space_to_delete and value<min_value:
            min_value=value
    return space_to_delete


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
