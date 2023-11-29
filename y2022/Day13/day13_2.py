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
    data = load_data(filepath, example=False).split("\n")
    remove_indices = []
    for i in range(len(data)):
        if data[i] == "":
            remove_indices.append(i)
    remove_indices.reverse()
    for index in remove_indices:
        data.pop(index)
    data = ['[[2]]']+data+['[[6]]']
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            left = eval(data[j])
            right = eval(data[j+1])
            if not compare_list(left, right):
                data[j], data[j+1] = data[j + 1], data[j]
    first = data.index('[[2]]')+1
    second = data.index('[[6]]')+1
    print(first*second)
    return print(data)

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
