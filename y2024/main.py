from day_imports import *

if __name__ == '__main__':
    set_cookie()
    todays_date = get_todays_date()
    insert_data(todays_date, 2024)
    exec("day{}_1.execution()".format(todays_date))
    exec("day{}_2.execution()".format(todays_date))
