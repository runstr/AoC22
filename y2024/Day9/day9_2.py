import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def create_index_map(data):
    ids = []
    _id = 0
    block_sizes = {}
    spaces = []
    spaces_start_index = []
    space_start_index = 0
    id_start_index = {}
    for i in range(len(data)):
        block_length = int(data[i])
        if i % 2 == 0:
            block_sizes[_id] = block_length
            id_start_index[_id] = space_start_index
            id_append = _id
            _id += 1
        else:
            id_append = -1
            spaces.append(block_length)
            spaces_start_index.append(space_start_index)
        space_start_index += block_length
        for _ in range(block_length):
            ids.append(id_append)
    return ids, block_sizes, spaces, spaces_start_index, id_start_index


def get_my_answer():
    my_answer = load_data(filepath, example=False)
    ids, block_sizes, spaces, spaces_start_index, id_start_index = create_index_map(my_answer)
    max_id = max(ids)
    done_sorting = False
    while True:
        block_size = block_sizes[max_id]
        for i in range(len(spaces)):
            if id_start_index[max_id] <= spaces_start_index[i]:
                break
            if block_size <= spaces[i]:
                spaces[i] -= block_size
                for j in range(block_size):
                    ids[spaces_start_index[i]+j] = max_id
                for k in range(block_size):
                    ids[id_start_index[max_id]+k] = -1
                spaces_start_index[i] += block_size
                break
        if done_sorting:
            break
        if max_id == 1:
            break
        max_id -= 1

    return check_checksum(ids)


def check_checksum(ids):
    check = ids
    total_sum = 0
    for index, _id in enumerate(check):
        if _id != -1:
            total_sum += int(_id)*index

    return total_sum


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
