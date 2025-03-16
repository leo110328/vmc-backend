from django.db import models


# 免疫程序实体
class ImmunizationInfo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, verbose_name="UUID")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    period_validity = models.CharField(max_length=32, verbose_name="有效期")
    vaccine_name = models.CharField(max_length=100, verbose_name="疫苗名称")
    vaccine_type = models.CharField(max_length=100, verbose_name="疫苗毒株")
    vaccine_batch = models.CharField(max_length=100, verbose_name="疫苗批次")
    vaccine_date = models.CharField(max_length=100, verbose_name="疫苗接种日期")
    vaccine_frequency = models.CharField(max_length=100, verbose_name="疫苗接种次数")
    vaccine_dosage = models.CharField(max_length=100, verbose_name="疫苗接种剂量")
    vaccine_route = models.CharField(max_length=100, verbose_name="疫苗接种途径")
    vaccine_manufacturers = models.CharField(max_length=100, verbose_name="疫苗制造商")
    vaccine_address = models.CharField(max_length=100, verbose_name="疫苗制造地")
    data_time = models.CharField(max_length=10, verbose_name="数据时间")
    data_version = models.IntegerField(verbose_name="数据版本")
    create_time = models.CharField(max_length=50, verbose_name="新增时间")
    create_by = models.CharField(max_length=32, verbose_name="新增人")
    update_time = models.CharField(max_length=50, verbose_name="更新时间")
    update_by = models.CharField(max_length=32, verbose_name="更新人")
    deleted = models.BooleanField(max_length=32, default=0, verbose_name="数据是否已删除[0:未删除,1:已删除]")

    class Meta:
        unique_together = (("id", "data_time", "data_version"),)
        db_table = "immunization_info"
