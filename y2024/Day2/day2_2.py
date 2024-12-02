import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def check_safe(report):

    if report[0] - report[1] == 0:
        return False

    if report[0] - report[1] < 0:
        increasing = True
    else:
        increasing = False
    safe = True
    for i, val in enumerate(report):
        if i == 0:
            continue
        if increasing:
            if report[i - 1] - val > -1 or report[i - 1] - val < -3:
                safe = False
                break
        else:
            if report[i - 1] - val < 1 or report[i - 1] - val > 3:
                safe = False
                break
    return safe


def get_my_answer():
    all_data = load_data_as_lines(filepath, example=True)
    num_safe = 0
    reports = []
    for line in all_data:
        line = list(map(int, line.split(" ")))
        reports.append(line)
    for report in reports:
        if check_safe(report):
            num_safe += 1
            continue
        safe = False
        for i in range(0, len(report)):
            new_report = report.copy()
            del new_report[i]
            if check_safe(new_report):
                safe = True
                break
        if safe:
            num_safe += 1
    print(num_safe)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
