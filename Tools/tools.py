from datetime import date
from aocd import get_data
from os import path, environ
import time


def set_cookie():
    with open("private.env", "r") as f:
        data = f.read()
        environ["AOC_SESSION"] = data.split("=")[1]


def load_data(filepath, example=False):
    if example:
        filepath = str(filepath)+"\\example.txt"
    else:
        filepath = str(filepath)+"\\input.txt"
    with open(filepath, "r") as f:
        data = f.read()
    return data


def load_data_as_lines(filepath, example=False):
    if example:
        filepath = str(filepath)+"\\example.txt"
    else:
        filepath = str(filepath)+"\\input.txt"
    with open(filepath, "r") as f:
        data = f.read().splitlines()
    return data


def load_data_as_int(filepath, example=False):
    if example:
        filepath = str(filepath)+"\\example.txt"
    else:
        filepath = str(filepath)+"\\input.txt"
    input_full = []
    with open(filepath, "r") as f:
        for input_line in f.read().splitlines():
            input_line_list = []
            for i in input_line:
                input_line_list.append(int(i))
            input_full.append(input_line_list)
    return input_full

def load_data_as_chars(filepath, example=False):
    if example:
        filepath = str(filepath)+"\\example.txt"
    else:
        filepath = str(filepath)+"\\input.txt"
    input_full = []
    with open(filepath, "r") as f:
        for input_line in f.read().splitlines():
            input_line_list = []
            for i in input_line:
                input_line_list.append(i)
            input_full.append(input_line_list)
    return input_full

def get_todays_date():
    return str(date.today().day)


def insert_data(todays_date):
    filename = __file__[:-14]+"Day"+todays_date+"\\input.txt"
    if path.getsize(filename) == 0:
        with open(filename, "w") as inputfile:
            inputfile.write(get_data(year=2022, day=int(todays_date)))


def timeexecution(function):
    def timed(*args, **kw):
        ts = time.time()
        result = function(*args, **kw)
        te = time.time()
        print("Time taken = {}".format(te-ts))
        return result
    return timed
