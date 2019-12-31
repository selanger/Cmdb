from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('idc/', IdcList.as_view(), name="idc"),  ## 资产机房信息
    # path('addidc/', AddIdc.as_view(), name="addidc"),  ## 增加资产机房
    # path('idc_update/', UpdateIdc.as_view(), name="idc_update"),  ## 更新资产机房信息
    # path('idc_delete/', DeleteIdc.as_view(), name="idc_delete"),  ## 更新资产机房信息
    path('host_list/', HostList.as_view(), name="host_list"),
    path('addhost/', AddHost.as_view(), name="host_add"),
    path('host_info/', HostInfo.as_view(), name="host_info"),
    path('host_delete/', DeleteHost.as_view(), name="host_delete"),
    path('host_update/', UpdateHost.as_view(), name="host_update"),
    path('create_task/', CreateTasks.as_view(), name="create_task"),
    path('task_order_list/', TaskOrderList.as_view(), name="task_order_list"),
    path('tancehost/', TanCeHost.as_view(), name="tancehost"),
    path('scan_list/', TanCeHostList.as_view(), name="scan_list"),
    path('task_update_host_status/', task_update_host_status),
    path('task_scan_ports_result/', csrf_exempt(task_scan_ports_result)),
    path('task_jietu_result/', csrf_exempt(task_jietu_result)),
    # path("add_idc/",addidc)
]
