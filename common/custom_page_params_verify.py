import json
import re

from django.utils.datastructures import MultiValueDictKeyError

from common.custom_response import error


def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
    return bool(pattern.match(string))


# 分页参数校验
def page_params_verify(request):
    try:
        request.query_params["page"]
    except MultiValueDictKeyError:
        return error("page不能為空")
    if not is_number(request.query_params["page"]):
        return error("page 格式不正確")
    try:
        request.query_params["size"]
    except MultiValueDictKeyError:
        return error("size不能為空")
    if not is_number(request.query_params["size"]):
        return error("size 格式不正確")
    return None
