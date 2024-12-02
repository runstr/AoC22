import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    all_data = load_data_as_lines(filepath, example=False)
    first_list, seconf_list = [], []
    for line in all_data:
        new_line = line.split("   ")
        first_list.append(int(new_line[0]))
        seconf_list.append(int(new_line[1]))
    similarity_score = 0
    for i in first_list:
        counts = seconf_list.count(i)
        similarity_score += i*counts
    print(similarity_score)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)