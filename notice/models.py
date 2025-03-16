from django.db import models


class NoticeInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    text = models.CharField(max_length=5000, verbose_name="消息内容")
    title = models.CharField(max_length=255, verbose_name="消息标题")
    msg_time = models.CharField(max_length=255, verbose_name="消息时间")
    resources_id = models.CharField(max_length=32, verbose_name="资源ID", null=True, blank=True)
    create_time = models.CharField(max_length=50, verbose_name="更新时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        db_table = "notice_info"
