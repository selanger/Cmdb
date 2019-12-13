from django.shortcuts import render
from django.views.generic import View,ListView
from django.contrib.auth.models import User, Group, Permission
from .models import Profile
from django.http import HttpResponse

# Create your views here.

## 用户列表
class UserList(ListView):
    """
    ListView 高级视图类，可以返回指定的页面，同时能够将数据进行整合 返回
    """

    template_name = "user_list.html"
    model = User
    paginate_by = 8     ## 开启分页，每页显示8条    通过get请求传递参数  page 进行获取第n页的数据
    """
    分页提供的方法
    page_obj.has_previous              判断是否有上一页
    page_obj.previous_page_number      上一页的页数对象
    page_obj.number                    当前页数
    page_obj.has_next                  判断是否有下一页
    page_obj.next_page_number          下一页的页面对象
    paginator.num_pages                最大页数
    paginator.page_range              可迭代的总页数
    """

    # def get_context_data(self, **kwargs):
    #     content = super(UserList, self).get_context_data(**kwargs)
    #     print(content)
    #     return content




### 批量增加数据
# class TestDataView(View):
#     def get(self, request):
#         # 存储基础表信息
#
#         for i in range(1, 100):
#             user = User()
#             user.username = "test{}".format(i)
#             user.password = 123456
#             user.email = "test{}@126.com".format(i)
#             user.save()
#             profile = Profile()
#             profile.profile_id = user.id
#             profile.name = "测试{}".format(i)
#             profile.wechat = "test{}".format(i)
#             profile.phone = "1520101010{}".format(i)
#             profile.info = "我是测试{}人员".format((i))
#             profile.save()
#         return HttpResponse('批量添加测试数据')




