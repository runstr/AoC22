import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()

def translate_source_to_dest(source_range, transform):
    source_start, source_end = source_range[0], source_range[1]
    for line in transform:
        if source >= line[1] and source <= line[1]+line[2]:
            destination = source-line[1]+line[0]
            return destination
    return source

def get_my_answer():
    data = load_data(filepath, example=True)
    data = data.split("\n\n")
    seeds = list(map(int, data[0].split(" ")[1:]))
    new_data = []
    for transform in data[1:]:
        new_transform = []
        for line in transform.split("\n")[1:]:
            new_transform.append(tuple(map(int, line.split(" "))))
        new_data.append(new_transform)
    old_source_range = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    for transform in new_data:
        new_source_range = []
        for source in old_source_range:
            new_source_range.append(translate_source_to_dest(source, transform))
        old_source_range = [i for i in new_source_range]
        print(new_source_range)


    return new_source_range

@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
