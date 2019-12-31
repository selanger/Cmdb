from django.db import models
from user.models import Company

HOST_STATUS = (
    (0, 'Unknown'),
    (1, 'up'),
    (2, 'down'),

)
SCAN_STATUS = (
    (0, '待探测'),
    (1, '正在探测'),
    (2, '探测成功'),
    (3, '探测失败')
)


## 主机
class Host(models.Model):
    """
    ip 资产信息
    """
    ip = models.CharField(max_length=32, verbose_name="主机ip")
    status = models.IntegerField(choices=HOST_STATUS, default=1, verbose_name="主机状态")
    scan_status = models.IntegerField(choices=SCAN_STATUS, default=0, verbose_name="主机探测状态")
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)


## 主机用户
class HostUser(models.Model):
    """
    主机用户
    """
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="登陆密码")
    host = models.ForeignKey(to=Host, on_delete=models.CASCADE)  ### 用户名和主机为一对多关系


#
class TasksOrder(models.Model):
    """
    扫描任务
    """
    order_no = models.CharField(max_length=36, verbose_name="订单号")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    # host = models.ForeignKey(to=Host,on_delete=models.CASCADE)
    celeryinfoid = models.IntegerField(verbose_name="CeleryInfo表的id", default=0)


class CeleryInfo(models.Model):
    task_id = models.TextField(verbose_name="celery任务id")
    time = models.DateTimeField(auto_now=True)

IMAGE_STATUS= (
    (0,'未确定'),
    (1,'高危'),
    (2,'安全')
)
class OrderInfo(models.Model):
    """
    扫描详情
    """
    order = models.ForeignKey(to=TasksOrder, on_delete=models.CASCADE)
    host = models.ForeignKey(to=Host, on_delete=models.CASCADE)
    # celeryinfo = models.ForeignKey(to=CeleryInfo, on_delete=models.CASCADE)
    port = models.IntegerField(verbose_name="扫描开发的端口号", null=True)
    image = models.CharField(max_length=256, null=True, verbose_name="截图之后图片路径")
    simple_image = models.CharField(max_length=256, null=True, verbose_name="相似图片路径")
    percent = models.FloatField(default=0,verbose_name="相似概率")
    status = models.IntegerField(default=0,verbose_name="图片状态")
class OpenPort(models.Model):
    host = models.ForeignKey(to=Host, on_delete=models.CASCADE)
    task_order = models.ForeignKey(to=TasksOrder, on_delete=models.CASCADE)
    port = models.CharField(max_length=32, verbose_name="端口")
    state = models.CharField(max_length=32, verbose_name="状态")
    reason = models.TextField(verbose_name="原因")
    extrainfo = models.TextField(verbose_name="额外信息")
    name = models.TextField(verbose_name="名字")
    version = models.TextField(verbose_name="版本")
    product = models.TextField(verbose_name="产品")
    cpe = models.TextField(verbose_name="CPE")
    script = models.TextField(verbose_name="脚本")
