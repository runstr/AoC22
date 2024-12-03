import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()


def get_my_answer():
    all_data = load_data(filepath, example=False)
    startet = False
    index = all_data.index("mul(")
    index = 0
    multiply_sequences = []
    total_number = 0
    dont = "don't()"
    dont_length = len(dont)
    do = "do()"
    do_length = len(do)
    disabled = False
    while index + 3 < len(all_data):
        try:
            if all_data[index:index+do_length] == do:
                disabled = False
                index += do_length
            elif all_data[index:index+dont_length] == dont:
                disabled = True
                index += dont_length
        except:
            pass

        if not disabled and all_data[index:index+4] == "mul(":
            mulitpication_text = ""
            start_index = index+4
            while all_data[start_index] != ")":
                mulitpication_text += all_data[start_index]
                start_index += 1
            try:
                first, last = mulitpication_text.split(",")
                first = int(first)
                last = int(last)
            except ValueError:
                pass
            else:
                total_number += (first * last)
                index=start_index
                multiply_sequences.append((first, last))
        index += 1
    print(multiply_sequences)
    return total_number


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
