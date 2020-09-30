import names
import time
import datetime


def time_machine():
    new_name = names.get_full_name()
    print(type(new_name))
    print(new_name)
    print(int(time.time()))
    data = 1601382467166482691
    print(datetime.datetime.fromtimestamp(data))


def string_tuple_to_dict(string: str):
    dict_fields = ["id", "img_path", "datetime", "cam_id", "p1", "p2", "name", "external_id"]

    string = string[1:-1].replace('"', '')
    string = string.split(',')
    del string[4:6]
    return dict(zip(dict_fields, string))


def list_comp():
    arr = ['(12,catches/4bb42eaa-112c-49f5-a192-1c0277ea7bc520200928-142646.jpg,"2020-09-28 14:26:46.770655+00","",'
           '5,5,"Betty Toms",4bb42eaa-112c-49f5-a192-1c0277ea7bc5)']

    res = [string_tuple_to_dict(string) for string in arr]
    print(res)


def get_today_midnight():
    today = datetime.date.today()
    midnight = datetime.datetime.combine(today, datetime.datetime.min.time())
    print(midnight)
    param = datetime.datetime.now()
    print(param.strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.datetime.now().replace(microsecond=0))


if __name__ == '__main__':
    # list_comp()
    get_today_midnight()

