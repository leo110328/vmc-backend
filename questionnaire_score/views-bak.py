import json

from rest_framework.decorators import api_view

from common.custom_response import error, ok
from common.time_utils import get_format_time
from common.token_utils import is_ordinary_users_login
from common.uuid_utils import get_uuid_str
from user.models import UserInfo
from user.serializers import UserInfoSerializer
from vmc_backend import settings
from .models import QuestionnaireScoreQueryInfo, QuestionnaireScoreInfo
from .serializers import QuestionnaireScoreInfoSerializer


# 获取最大版本数据
def get_mxa_version_data(farm_id, user_id):
    sql = " SELECT 	t1.*  FROM 	questionnaire_score_info t1 INNER JOIN ( SELECT t.id, t.farm_id, MAX( t.data_version ) AS data_version, t.user_id FROM questionnaire_score_info t WHERE 1 = 1 "
    if user_id is not None:
        sql += " AND t.user_id = '%s' " % user_id
    if farm_id is not None:
        sql += " AND t.farm_id = '%s' " % farm_id
    sql += " ORDER BY t.id ) t2 ON t1.data_version = t2.data_version and  t1.id = t2.id "
    if settings.DEBUG:
        print("查询当前问卷得分信息最大版本数据,sql = {}".format(sql))
    roles = QuestionnaireScoreInfo.objects.raw(sql)
    if len(roles) <= 0:
        return None
    return roles[0]


@api_view(['POST'])
def add(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")
    data = json.loads(request.body)
    if "farmId" not in data:
        return error("farmId 不能為空")
    if "totalScore" not in data:
        return error("totalScore 不能為空")
    user_info = UserInfo.objects.filter(id=data['farmId'])
    if len(user_info) == 0:
        return error("农场不存在")
    info = get_mxa_version_data(data["farmId"], user_id)
    data_version = '0' if info is None else info.data_version
    id = get_uuid_str() if info is None else info.id
    QuestionnaireScoreInfo.objects.create(id=id, farm_id=data["farmId"], user_id=user_id,
                                          total_score=data["totalScore"],
                                          data_version=int(data_version) + 1,
                                          create_time=get_format_time(),
                                          create_by=user_id,
                                          update_time=get_format_time(),
                                          update_by=user_id,
                                          deleted='0',
                                          )
    return ok("成功")


@api_view(['POST'])
def query_total_score(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")

    data = json.loads(request.body)
    sql = "select * from user_info where deleted = '0' "
    if "farmId" in data:
        sql += " and id =  '%s' " % data["farmId"]
    if settings.DEBUG:
        print("查询所有农场信息,sql = {}".format(sql))
    user_roles = UserInfo.objects.raw(sql)
    user_roles_ser = UserInfoSerializer(user_roles, many=True)

    result = []
    for user in user_roles_ser.data:
        sql = " SELECT 	t1.*,u.username  FROM 	questionnaire_score_info t1 INNER join user_info u on t1.farm_id = u.id where 1 = 1 "
        if "userId" in data:
            sql += " AND t1.user_id = '%s' " % data["userId"]
        sql += "  order by total_score"
        if settings.DEBUG:
            print("查询所有农场问卷得分信息,sql = {}".format(sql))
        score_roles = QuestionnaireScoreQueryInfo.objects.raw(sql)
        score_roles_ser = QuestionnaireScoreInfoSerializer(score_roles, many=True)
        result.append({"farmId": user["id"], "farmIdName": user["farmName"], "scores": score_roles_ser.data})
    return ok(result)


@api_view(['POST'])
def query_answer_list(request):
    user_id = is_ordinary_users_login(request)
    if user_id is None:
        return error("未登錄")

    sql = " SELECT 	t1.*,u.username  FROM 	questionnaire_score_info t1 INNER JOIN ( SELECT t.id, t.farm_id, MAX( t.data_version ) AS data_version, t.user_id FROM questionnaire_score_info t WHERE 1 = 1 "
    sql += " AND t.user_id = '%s' " % user_id
    sql += " ORDER BY t.id ) t2 ON t1.data_version = t2.data_version and  t1.id = t2.id INNER join user_info u on t1.farm_id = u.id"
    if settings.DEBUG:
        print("查询当事人回答问卷列表,sql = {}".format(sql))
    roles = QuestionnaireScoreQueryInfo.objects.raw(sql)
    roles_ser = QuestionnaireScoreInfoSerializer(roles, many=True)
    return ok(roles_ser.data)
