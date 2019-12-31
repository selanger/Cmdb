from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *
from django.urls import reverse
import uuid
import time
from .tasks import checkIP, scan_ports, screenshot
from user.models import Company
import json
from celery.result import AsyncResult


def get_orderno():
    order_id = str(uuid.uuid4())
    return order_id



class HostList(ListView):
    template_name = "host_list.html"
    model = Host
    paginate_by = 8

    def get_context_data(self, **kwargs):
        content = super(HostList, self).get_context_data(**kwargs)
        content['page_range'] = self.page_range(content['page_obj'], content["paginator"])  ### 将生成的页码返回

        return content

    def page_range(self, page_obj, paginator):
        ### 只显示5个页码
        current_index = page_obj.number  ### 获取当前页码    3 5 8
        start = current_index - 2
        end = current_index + 3
        if start <= 2:
            start = 1
            end = 6
            if end > paginator.num_pages:
                end = paginator.num_pages + 1
        elif end > paginator.num_pages:
            end = paginator.num_pages + 1
            start = end - 5

        return range(start, end)


## 录入资产
class AddHost(TemplateView):
    template_name = "addhost.html"

    def get_context_data(self, **kwargs):
        content = super(AddHost, self).get_context_data(**kwargs)
        ## 机房信息
        content['com_obj'] = self.getCom()  ### 将生成的页码返回
        return content

    def getCom(self):
        data = Company.objects.all()
        return data

    def post(self, request):
        ## 获取资产信息，并录入
        data = request.POST
        print(data)
        ip = request.POST.get("ip")
        company = request.POST.get("company", None)
        if not company:
            return HttpResponse("单位必须")
        checked = request.POST.get("checked", None)  ## 是否开启主机探测
        scan_status = 0
        if checked:
            scan_status = 1  ## 开启探测

        host = Host.objects.create(
            ip=ip,
            scan_status=scan_status,
            company_id=int(company)
        )

        ## 保存登陆主机账号 密码
        username = request.POST.get("username")
        if username:
            HostUser.objects.create(
                username=username,
                password=request.POST.get("password"),
                host=host
            )

        if scan_status == 1:
            ## 发送探测异步任务
            params = {
                "ip": ip
            }
            result = checkIP.delay(params)
            CeleryInfo.objects.create(
                task_id=result.id
            )

        return HttpResponseRedirect(reverse("host_list"))


def task_update_host_status(request):
    ### 异步任务修改主机状态
    ## 主机状态默认为： 开启，如果探测失败，则请求 修改状态为 关闭

    ip = request.GET.get("ip")
    Host.objects.filter(ip=ip).update(status=2)
    result = {"code": 10000}
    return JsonResponse(result)


## 查看更多资产信息
class HostInfo(TemplateView):
    template_name = "host_info.html"

    def get_context_data(self, **kwargs):
        content = super(HostInfo, self).get_context_data(**kwargs)
        content["host_object"] = self.gethost(self.request)
        return content

    def gethost(self, request):
        # print(request.GET.get("id"))
        id = request.GET.get("id")
        host = Host.objects.get(id=int(id))
        return host


## 删除资产信息
class DeleteHost(View):

    def post(self, request):
        res = {"code": 10000, "msg": "删除成功"}
        id = request.POST.get("id")
        # Idc.objects.filter(id=id).delete()
        Host.objects.filter(id=id).delete()

        return JsonResponse(res)


class UpdateHost(TemplateView):
    template_name = 'update_host.html'

    def get_context_data(self, **kwargs):
        content = super(UpdateHost, self).get_context_data(**kwargs)
        content["host_obj"], content["host_user"] = self.get_host(self.request)
        content["idc"] = self.getallidc()

        return content

    def get_host(self, request):
        id = request.GET.get("id")
        data = Host.objects.filter(id=int(id)).first()
        ## 账号名字
        username = []
        hostuser = data.hostuser_set.all()
        for user in hostuser:
            username.append(user.username)

        return data, username

    def getallidc(self):
        # idc = Idc.objects.all()
        idc = ""
        return idc


# def addidc(request):
#     for one in range(100):
#         Idc.objects.create(
#             idc_name="name_%s" % one,
#             idc_name_all="idc_name_all_%s" % one,
#             address="address_%s" % one,
#             phone="phone_%s" % one,
#             name="name_%s" % one,
#             email="email_%s" % one
#         )
#
#     return HttpResponse("add idc")


class CreateTasks(ListView):
    template_name = "createtasks.html"
    model = Host

    def post(self, request):
        ## 添加任务
        ## 条件: 对应主机探测过端口，并且状态为up状态
        result = {"code": 10000, "msg": "添加任务成功"}
        host = request.POST.getlist("data[]", None)  ## 以列表的形式获取选中的host id
        if not host:
            result = {"code": 10001, "msg": "请选择ip"}
            return JsonResponse(result)
        host_id = list(map(int, host))  ## 将获取到的host id 列表中的元素转化为 int

        ip_all = Host.objects.filter(id__in=host_id).values("ip")  ##  获取选中的ip值
        # 创建异步任务
        order_no = get_orderno()
        params = {
            "ip_list": get_port(ip_all),
            "order_no": order_no
        }
        task_result = screenshot.delay(params)
        ci = CeleryInfo.objects.create(
            task_id=task_result.id
        )

        ##生成订单
        TasksOrder.objects.create(
            order_no=order_no,
            celeryinfoid=ci.id
        )

        # ## TasksOrder
        # ## 生成订单
        # for one in ip_all:
        #     print(one)
        #     ## 添加截图任务

        return JsonResponse(result)


## 获取开放的端口
def get_port(ip_all):
    result = []
    for ip in ip_all:
        ports = OpenPort.objects.filter(state="up", host__ip=ip).values("port")
        result.append(dict(ip=ip, ports=ports))
    return result

    ### 创建任务
    ## 拿到系统中所有的ip地址信息
    ## 选择需要探测的ip
    ## 生成任务，开始进行后台任务探测
    ## 先探测开启的端口
    ## 探测服务
    ## 截图  保存


class TaskOrderList(ListView):
    template_name = "taskorderlist.html"
    model = TasksOrder
    paginate_by = 8

    def get_context_data(self, **kwargs):
        content = super(TaskOrderList, self).get_context_data(**kwargs)
        content['page_range'] = self.page_range(content['page_obj'], content["paginator"])  ### 将生成的页码返回

        return content

    def page_range(self, page_obj, paginator):
        ### 只显示5个页码
        current_index = page_obj.number  ### 获取当前页码    3 5 8
        start = current_index - 2
        end = current_index + 3
        if start <= 2:
            start = 1
            end = 6
            if end > paginator.num_pages:
                end = paginator.num_pages + 1
        elif end > paginator.num_pages:
            end = paginator.num_pages + 1
            start = end - 5

        return range(start, end)


## 扫描存活ip
## 扫描端口

class TanCeHost(View):
    def post(self, request):
        id = request.POST.get("id")
        host = Host.objects.get(id=int(id))

        order_no = str(time.time()).replace(".", "")
        ## 创建异步扫描任务
        result = scan_ports.delay({"ip": host.ip, "order_no": order_no})
        ci = CeleryInfo.objects.create(
            task_id=result.id
        )

        taskorder = TasksOrder.objects.create(
            order_no=order_no,
            celeryinfoid=ci.id
        )
        return JsonResponse({"code": 10000, "msg": "添加任务成功"})


def task_scan_ports_result(request):
    # order_no = request.GET.get("order_no")
    # # print (order_no)
    # taskorder = TasksOrder.objects.get(order_no=order_no)
    # celeryid = CeleryInfo.objects.get(id=taskorder.celeryinfoid).task_id
    # print(celeryid)
    #
    # ## 读取celery中的结果
    # res = AsyncResult(celeryid)  # 参数为task id
    # print(res.result)

    port_list = ["22", "3306"]
    data = request.body
    data = json.loads(data.decode())
    order_no = data.get("order_no")
    status = data.get("status")
    if status == 'down':
        ## 主机关闭状态
        pass
    elif status == "up":
        ## 开启状态
        taskorder = TasksOrder.objects.get(order_no=order_no)
        host = taskorder.host
        host.status = 1
        host.scan_status = 2
        host.save()

        for port in data.get("ports"):
            if port["port"] not in port_list:
                OpenPort.objects.create(
                    host=host,
                    task_order=taskorder,
                    port=port["port"],
                    state=port["state"],
                    reason=port["reason"],
                    extrainfo=port["extrainfo"],
                    name=port["name"],
                    version=port["version"],
                    product=port["product"],
                    cpe=port["cpe"],
                    script=port["script"]
                )

    ## 写库
    return JsonResponse({"code": 10000})


## 主机探测列表
class TanCeHostList(ListView):
    template_name = "scan_list.html"
    model = TasksOrder
    paginate_by = 8

    def get_context_data(self, **kwargs):
        content = super(TanCeHostList, self).get_context_data(**kwargs)
        content['page_range'] = self.page_range(content['page_obj'], content["paginator"])  ### 将生成的页码返回

        return content

    def page_range(self, page_obj, paginator):
        ### 只显示5个页码
        current_index = page_obj.number  ### 获取当前页码    3 5 8
        start = current_index - 2
        end = current_index + 3
        if start <= 2:
            start = 1
            end = 6
            if end > paginator.num_pages:
                end = paginator.num_pages + 1
        elif end > paginator.num_pages:
            end = paginator.num_pages + 1
            start = end - 5

        return range(start, end)

import os
def task_jietu_result(request):
    data = request.body
    data = json.loads(data.decode())
    order_no = data.get("order_no")
    info = data.get("info")
    for one in info:
        ip = one.get("ip")
        port = one.get("port")
        imagename = os.path.join(order_no,one.get("imagename"))
        ## 写库
        OrderInfo.objects.create(
            order = TasksOrder.objects.get(order_no = order_no),
            host = Host.objects.get(ip = ip),
            port = port,
            image = imagename

        )
    simple_image(order_no)

    return JsonResponse({"code": 10000})


## 相似图片比对
def simple_image(order_no):
    ##
    pass


