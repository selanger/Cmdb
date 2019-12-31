from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


### LoginRequiredMixin django提供的登陆验证类
## 需要在settings中增加验证失败之后要跳转的登陆页面路由，即settings中的 LOGIN_URL 配置
class Index(LoginRequiredMixin,View):

    def get(self, request):
        return render(request, "index.html")


class Login(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        ## user 对象，可以获取其中的属性
        if user:
            login(request, user)  ### 如果校验成功，执行登陆函数， 并设置session
            return HttpResponseRedirect(reverse("index"))
        else:
            ## 登录失败
            return HttpResponseRedirect(reverse("login"))


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


from django.http import HttpResponse


def getresult(request):
    from celery.result import AsyncResult

    res = AsyncResult("444d09a8-3407-4fe8-a898-64cb84432232")  # 参数为task id
    print(res.result)

    return HttpResponse("jieguo ")
