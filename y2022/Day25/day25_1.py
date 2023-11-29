import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit

filepath = pathlib.Path(__file__).parent.resolve()

#Shifted by two, we get the following
SNAFU_TO_DEC = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
DEC_TO_SNAFU = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}
REM_TO_SNAFU = {3: "=", 4: "-", 0: "0", 1: "1", 2: "2"}


def snafu_to_decimal(snafu_number):
    decimal = 0
    for i in range(len(snafu_number)):
        decimal += (5**(len(snafu_number)-i-1))*SNAFU_TO_DEC[snafu_number[i]]
    return decimal


def find_length(decimal_number):
    i = 0
    total = 0
    while True:
        total += 2*5**i
        if total >= decimal_number:
            break
        i+=1
    return i+1

def max_number(i):
    number = 5**i
    for j in range(i-1, -1,-1):
        number+=2*5**j
    return number


def decimal_to_snafu_converter(decimal_number, length_of_number):
    snafu = ""
    i = length_of_number-1
    while i >= 0:
        if decimal_number >= 0:
            if decimal_number > max_number(i):
                snafu = snafu+"2"
                decimal_number -= 2*5**i
            elif decimal_number > 2*5**(i-1):
                snafu = snafu + "1"
                decimal_number -= 5 ** i
            else:
                snafu = snafu + "0"
        else:
            if abs(decimal_number) > max_number(i):
                snafu = snafu+"="
                decimal_number += 2*5**i
            elif abs(decimal_number) > 2*5 ** (i - 1):
                snafu = snafu + "-"
                decimal_number += 5 ** i
            else:
                snafu = snafu + "0"
        i -= 1
    return snafu

def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    #data = ["1", "2", "1=", "1-", "10", "11", "12", "2=", "2-"]
    total_sum = 0
    for snafu_number in data:
        decimal_number = snafu_to_decimal(snafu_number)
        total_sum+=decimal_number
        length_of_number = find_length(decimal_number)
        snaf = decimal_to_snafu_converter(decimal_number, length_of_number)
        #print(decimal_number, " : ", snaf)
    length_of_number = find_length(total_sum)
    snaf = decimal_to_snafu_converter(total_sum, length_of_number)
    return snaf


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2022)
