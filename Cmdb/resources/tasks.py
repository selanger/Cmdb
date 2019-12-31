from __future__ import absolute_import
from Cmdb.celery import app
from sdk.nmapsdk import NmapSdk
from sdk.jietu import JieTu
from .models import *



### 检测主机是否存活
@app.task
def checkIP(params):
    job = NmapSdk(params)
    result = job.checkOneIP()
    return result

## 扫描up主机存活端口
@app.task
def scan_ports(params):
    """

    :param params:
            ip
            order_no
    :return:
    """
    job = NmapSdk(params)
    result = job.checkPort()
    # print (1111)
    return result


# 并且针对存活端口进行首页截图
@app.task
def screenshot(params):
    job = JieTu(params)
    result = job.run()
    return result
