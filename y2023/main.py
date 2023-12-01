from day_imports import *

if __name__ == '__main__':
    set_cookie()
    todays_date = "1" # = get_todays_date()
    #insert_data(todays_date, 2023)
    exec("day{}_1.execution()".format(todays_date))
    exec("day{}_2.execution()".format(todays_date))
