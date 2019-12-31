from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from .models import Profile, Company
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


## 单位
class CompanyList(ListView):
    """
    ListView 高级视图类，可以返回指定的页面，同时能够将数据进行整合 返回
    """

    template_name = "company_list.html"
    model = Company
    paginate_by = 8  ## 开启分页，每页显示8条    通过get请求传递参数  page 进行获取第n页的数据

    def get_context_data(self, **kwargs):
        content = super(CompanyList, self).get_context_data(**kwargs)
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


## 增加单位
class CompanyAddView(TemplateView):
    template_name = "company_add.html"

    def post(self, request):
        company = request.POST.get("company")
        address = request.POST.get("address")
        com = Company.objects.filter(company=company).first()
        if com:
            return HttpResponse("已存在")

        Company.objects.create(
            company=company,
            address=address
        )
        url = request.META.get("HTTP_REFERER")

        return HttpResponseRedirect(url)


## 增加单位
class CompanyDeleteView(View):

    def post(self, request):
        ## 删除单位
        com_id = request.POST.get("com_id")
        Company.objects.filter(id=com_id).delete()
        result = {"code": 10000, "msg": "delete"}
        return JsonResponse(result)


## 用户列表
class UserList(ListView):
    """
    ListView 高级视图类，可以返回指定的页面，同时能够将数据进行整合 返回
    """

    template_name = "user_list.html"
    model = User
    paginate_by = 8  ## 开启分页，每页显示8条    通过get请求传递参数  page 进行获取第n页的数据
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

    def get_context_data(self, **kwargs):
        content = super(UserList, self).get_context_data(**kwargs)
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

## 增加用户
class UserAddView(TemplateView):
    template_name = "user_add.html"

    def get_context_data(self, **kwargs):
        content = super(UserAddView, self).get_context_data(**kwargs)
        id = self.request.GET.get('id')
        content['com_obj'] = Company.objects.all()

        return content

    def post(self, request):
        username = request.POST.get("username")
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("name")
        QQ = request.POST.get("QQ")
        com = request.POST.get("company")
        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email
        )
        Profile.objects.create(
            name=name,
            QQ=QQ,
            phone=phone,
            profile=user,
            company_id=int(com)
        )

        url = request.META.get("HTTP_REFERER")

        return HttpResponseRedirect(url)


### 修改用户信息
class UserUpdate(TemplateView):
    template_name = "user_update.html"

    def get_context_data(self, **kwargs):
        content = super(UserUpdate, self).get_context_data(**kwargs)
        id = self.request.GET.get('id')
        content['user_obj'] = User.objects.get(id=id)

        return content

    def post(self, request):
        # print (request.POST)
        uid = request.POST.get('uid')
        ##更新数据
        user = User.objects.filter(id=uid).first()
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        if request.POST.get("password") != "***":
            user.password = make_password(request.POST.get('password'))
        user.save()

        Profile.objects.filter(profile_id=uid).update(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            QQ=request.POST.get('QQ'),
            company=request.POST.get('company'),
        )

        url = request.META.get("HTTP_REFERER")

        return HttpResponseRedirect(url)


## 用户是否激活使用
class UserPermissions(View):
    def get(self, request):
        id = request.GET.get("id")

        user = User.objects.get(id=int(id))
        if user.is_active:
            user.is_active = 0
        else:
            user.is_active = 1

        user.save()
        return JsonResponse({"code": 10000, "msg": "更新成功"})
