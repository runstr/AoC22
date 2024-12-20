import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

def rules(number):
    """
    If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone
    """
    if number == "0":
        return ["1"]
    if len(number) % 2 == 0:
        return [str(int(number[:len(number)//2])), str(int(number[len(number)//2:]))]
    return [str(int(number)*2024)]


def get_my_answer():
    data = load_data(filepath, example=False).split(" ")
    i=0
    new_list = data
    while i < 25:
        old_list = new_list
        new_list = []
        for j in old_list:
            new_list += rules(j)
        i+=1
    return len(new_list)


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
