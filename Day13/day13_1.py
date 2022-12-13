import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def compare_list(left, right, not_correct_order):
    for i in range(len(right)):
        try:
            a = left[i]
        except IndexError:
            return True
        if type(left[i]) == list and type(right[i]) == int:
            right = [right[i]]
            not_correct_order = compare_list(left[i], right, False)
            if not_correct_order:
                return not_correct_order
            else:
                continue
        elif type(left[i]) == int and type(right[i]) == list:
            left = [left[i]]
            not_correct_order=compare_list(left, right[i], False)
            if not_correct_order:
                return not_correct_order
            else:
                continue
        elif type(left[i]) == list and type(right[i]) == list:
            not_correct_order = compare_list(left[i], right[i], False)
            if not_correct_order:
                return not_correct_order
            else:
                continue
        if len(left) < len(right):
            not_correct_order = True
            return not_correct_order
        if left[i]>right[i]:
            return not_correct_order
    return not_correct_order




def get_my_answer():
    data = load_data(filepath, example=False).split("\n\n")
    sum_indices=0
    for i, packet in enumerate(data):
        left, right = packet.split("\n")
        left = eval(left)
        right = eval(right)
        not_correct_order = compare_list(left, right, False)
        if not_correct_order:
            sum_indices+=(i+1)
        print(sum_indices)

    return sum_indices


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
