from django.db import models


class UserInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    username = models.CharField(max_length=255, verbose_name="用户名")
    password = models.CharField(max_length=255, verbose_name="密码")
    email = models.CharField(max_length=255, verbose_name="邮箱")
    phone = models.CharField(max_length=255, verbose_name="电话号码")
    farm_name = models.CharField(max_length=255, verbose_name="农场名称")
    sex = models.CharField(max_length=2, verbose_name="性别", null=True, blank=True)
    last_logon_time = models.CharField(max_length=50, verbose_name="上次登錄时间")
    is_admin = models.CharField(max_length=1, verbose_name="是否是管理员[0:不是,1:是]")
    status = models.CharField(max_length=2, verbose_name="状态[0:停用,1:启用]")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        db_table = "user_info"
