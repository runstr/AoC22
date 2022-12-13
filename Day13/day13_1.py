import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def compare_list(left, right):
    for i in range(len(left)):
        try:
            if type(left[i]) == list and type(right[i]) == int:
                return_value = compare_list(left[i], [right[i]])
                if return_value == None:
                    continue
                else:
                    return return_value
            elif type(left[i]) == int and type(right[i]) == list:
                return_value =  compare_list([left[i]], right[i])
                if return_value == None:
                    continue
                else:
                    return return_value
            elif type(left[i]) == list and type(right[i]) == list:
                return_value = compare_list(left[i], right[i])
                if return_value == None:
                    continue
                else:
                    return return_value
            if left[i] > right[i]:
                return False
            elif left[i] < right[i]:
                return True
        except IndexError:
            return False
    try:
        right[len(left)]
    except IndexError:
        return None
    return True


def get_my_answer():
    data = load_data(filepath, example=False).split("\n\n")
    sum_indices=0
    for i, packet in enumerate(data):
        left, right = packet.split("\n")
        left = eval(left)
        right = eval(right)
        correct_order = compare_list(left, right)
        if correct_order:
            sum_indices += (i+1)
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
