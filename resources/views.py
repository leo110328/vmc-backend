import json
import os
import time

from django.http import HttpResponse
from rest_framework.decorators import api_view
from django import forms
from django.db.models import Q

from common.custom_page_params_verify import page_params_verify
from common.custom_response import error, ok, ok_page
from common.time_utils import get_format_time
from common.token_utils import is_admin_users_login, is_ordinary_users_login
from common.uuid_utils import get_uuid_str, get_default_id
from resources.models import ResourcesInfo
from resources.serializers import ResourcesInfoSerializer
from common.custon_page_conf.custom_page import CustomPagePagination
from vmc_backend import settings


class UploadFileForm(forms.Form):
    file = forms.FileField()


# 保存文件到本地
def save_file_local(request):
    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return None
    file = form.cleaned_data['file']
    file_type = file.name[file.name.index(".") + 1:]
    file_name = str(int(round(time.time() * 1000))) + file.name[file.name.index("."):]
    file_path = settings.MEDIA_ROOT
    # 将文件保存到指定位置
    with open(os.path.join(file_path, file_name), 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return {"fileType": file_type, "filePath": file_path, "fileName": file_name}


@api_view(['POST'])
def addFile(request):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    fileInfo = save_file_local(request)
    if fileInfo is None:
        return error("文件无效")
    uuid = get_uuid_str()
    save_resources(uuid, "1", fileInfo["fileType"], fileInfo["fileName"], fileInfo["filePath"], user_id)
    return ok("成功")


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    fileInfo = save_file_local(request)
    if fileInfo is None:
        return error("文件无效")
    uuid = get_uuid_str()
    save_resources(uuid, "0", fileInfo["fileType"], fileInfo["fileName"], fileInfo["filePath"], user_id)
    return ok({"id": uuid, "type": fileInfo["fileType"]})


@api_view(['POST'])
def query_page(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    if not page_params_verify(request) is None:
        return page_params_verify(request)
    roles = ResourcesInfo.objects.filter(Q(resources_type="1"))
    page_roles = CustomPagePagination().paginate_queryset(queryset=roles, request=request)
    roles_ser = ResourcesInfoSerializer(page_roles, many=True)
    return ok_page(request, roles.__len__(), roles_ser.data)


@api_view(['GET'])
def delete(request, id):
    user_id = is_admin_users_login(request)
    if user_id is None:
        return error("沒有許可權")
    resources_info = ResourcesInfo.objects.filter(Q(resources_type="1") & Q(id=id))
    if len(resources_info) <= 0:
        return error("文件不存在")
    resources_info.delete()
    return ok("成功")


def download(request, id):
    resources_info = ResourcesInfo.objects.filter(id=id)
    if len(resources_info) == 0:
        return HttpResponse(json.dumps({"message": 'success', "code": '-1', "data": "资源不存在"}),
                            content_type="application/json")
    path = os.path.join(resources_info[0].path, resources_info[0].name)
    if not os.path.exists(path):
        return HttpResponse(json.dumps({"message": 'success', "code": '-1', "data": "资源不存在"}),
                            content_type="application/json")
    file_stream = open(path, 'rb')
    response = HttpResponse(file_stream.read())
    file_stream.close()
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        os.path.basename(resources_info[0].name))
    return response


def save_resources(uuid, resources_type, file_type, file_name, file_path, user_id):
    ResourcesInfo.objects.create(id=uuid, name=file_name,
                                 path=file_path,
                                 resources_type=resources_type,
                                 file_type=file_type, person=get_default_id(), remarks="",
                                 create_time=get_format_time(),
                                 create_by=user_id,
                                 update_time=get_format_time(),
                                 update_by=user_id,
                                 deleted='0',
                                 )
