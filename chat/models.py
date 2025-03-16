from django.db import models


class MsgInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    send_id = models.CharField(max_length=32, verbose_name="发送人ID")
    send_name = models.CharField(max_length=255, verbose_name="发送人名称")
    accept_id = models.CharField(max_length=32, verbose_name="接受人ID")
    msg_id = models.CharField(max_length=32, verbose_name="消息ID")
    msg_type = models.CharField(default="1", max_length=32, verbose_name="消息类型")
    msg_value = models.CharField(max_length=255, verbose_name="消息内容")
    timestamp = models.CharField(max_length=255, verbose_name="消息接收时间")
    send_success = models.CharField(default="0", max_length=1, verbose_name="是否以发送给对应的用户")

    class Meta:
        db_table = "chat_msg_info"
