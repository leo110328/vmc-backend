from rest_framework import status
from rest_framework.response import Response

from common.custon_page_conf.custom_page import CustomPagePagination


def get_total_page(len, size):
    if (len % size) == 0:
        return int(len / size)
    else:
        return int(len / size) + 1


# 返回分页查询对象

def ok_page(request, total_number, data):
    page = request.query_params["page"]
    size = request.query_params["size"]
    if int(size) > CustomPagePagination().max_page_size:
        size = CustomPagePagination().max_page_size
    page = {"page": page, "size": size, "totalNumber": total_number,
            "totalPage": get_total_page(int(total_number), int(size))}
    return Response({"message": 'success', "code": '0', "data": [{"page": page, "list": data}]},
                    status=status.HTTP_200_OK)


# 返回对象
def ok(data):
    return Response({"message": 'success', "code": '0', "data": data}, status=status.HTTP_200_OK)


def ok_all_date(data):
    result = []
    for index in data:
        result.append(index["dataTime"])
    return Response({"message": 'success', "code": '0', "data": result}, status=status.HTTP_200_OK)


def error(data):
    return Response({"message": 'success', "code": '-1', "data": data}, status=status.HTTP_200_OK)
