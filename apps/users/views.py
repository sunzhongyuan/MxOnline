# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm
# Create your views here.


class CustomBackend(ModelBackend):  # 自定义登陆方式 继承ModelBackend 把这个类配到settings里才会生效
    def authenticate(self, username=None, password=None, **kwargs):     # 重写authenticate
        try:
            #
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用类做为view Django常用   用法 LoginView.as_view()
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)    # 校验表单字段 标准是LoginForm这个类 属性一一对应进行校验
        if login_form.is_valid():   # 如果校验通过
            user_name = request.POST.get('username', '')  # 获取用户名
            pass_word = request.POST.get('password', '')  # 获取密码
            # 到表里查找用户密码 有数据返回UserProfile类 没查到返回None
            # authenticate方法默认验证用户名密码 可重写该方法进行自定义 比如用邮箱和密码登陆
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)  # 登陆  login是django提供的登陆方法  user信息会放到request里 传到页面
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 函数做为view 可以用Django自带的view类替代
# def user_login(request):    # 登陆功能的view
#     if request.method == 'POST':    # 表单提交了 接收用户登陆信息 并验证
#         user_name = request.POST.get('username', '')    # 获取用户名
#         pass_word = request.POST.get('password', '')    # 获取密码
#         # 到表里查找用户密码 有数据返回UserProfile类 没查到返回None
#         # authenticate方法默认验证用户名密码 可重写该方法进行自定义 比如用邮箱和密码登陆
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)    # 登陆  login是django提供的登陆方法  user信息会放到request里 传到页面
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     elif request.method == 'GET':   # 跳转到登陆页面
#         return render(request, 'login.html', {})
