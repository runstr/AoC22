import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    data = list(map(int, load_data_as_lines(filepath, example=False)))
    original_list = []
    new_list=[]
    for i, number in enumerate(data):
        number = number*811589153
        number = number + abs(i/(len(data)+1)) if number >= 0 else number - abs(i/(len(data)+1))
        original_list.append(number)
        new_list.append(number)
    for _ in range(10):
        for val in original_list:
            index = new_list.index(val)
            new_index = index+int(val) % (len(original_list)-1) if val >= 0 else index-abs(int(val)) % (len(original_list)-1)
            if new_index > len(original_list)-1:
                new_index -= (len(original_list)-1)
            if new_index == 0 and index > new_index:
                new_index = len(original_list)
            new_list.pop(index)
            new_list.insert(new_index, val)
    new_list = [int(val) for val in new_list]
    value1 = new_list[(new_list.index(0) + 1000) % len(original_list)]
    value2 = new_list[(new_list.index(0) + 2000) % len(original_list)]
    value3 = new_list[(new_list.index(0) + 3000) % len(original_list)]
    print(sum([value1, value2, value3]))
    return data


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2022)
