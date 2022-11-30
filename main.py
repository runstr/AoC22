import DefaultDay.day1_1
from day_imports import *
from Tools import *

if __name__ == '__main__':
    #DefaultDay.day1_1.execution()
    #todays_date = get_todays_date()
    insert_data(todays_date)
    todays_date = 1
    exec("day{}_1.execution()".format(todays_date))
    exec("day{}_2.execution()".format(todays_date))
