from django.db import models


class ResourcesInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    name = models.CharField(verbose_name="资源名称", max_length=255, null=True, blank=True)
    path = models.TextField(verbose_name="资源存放路径")
    resources_type = models.CharField(max_length=2, verbose_name="资源类型[0:消息附件],1:表格附件")
    file_type = models.CharField(max_length=50, verbose_name="文件类型", null=True, blank=True)
    person = models.CharField(max_length=32, verbose_name="所属管理员ID")
    remarks = models.TextField(verbose_name="备注", null=True, blank=True)
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        db_table = "resources_info"
