import time
from datetime import datetime


def get_format_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_int_time():
    return int(time.mktime(time.localtime(time.time())))


# 判断时间是否是yyyy-mm-dd格式
def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    print(get_format_time())
    print(get_int_time())
