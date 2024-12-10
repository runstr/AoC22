import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()
def create_index_map(data):
    ids = []
    id=0
    for i in range(len(data)):
        block_length = int(data[i])
        if i % 2 == 0:
            id_append = id
            id += 1
        else:
            id_append = -1
        for _ in range(block_length):
            ids.append(id_append)
    return ids

def get_my_answer():
    my_answer = load_data(filepath, example=False)
    ids = create_index_map(my_answer)
    new_ids = []
    end_index = len(ids) - 1
    start_index = 0
    while True:
        if start_index > end_index:
            break
        start_id = ids[start_index]
        end_id = ids[end_index]
        if end_id == -1:
            end_index -= 1
            continue
        if start_id == -1:
            new_ids.append(end_id)
            end_index -= 1
            start_index += 1
        else:
            new_ids.append(start_id)
            start_index += 1
    total_sum = 0
    for index, id in enumerate(new_ids):
        total_sum += (id*index)
    #print(new_ids)


    return total_sum


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
