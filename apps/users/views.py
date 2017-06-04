# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View  # view类
from django.contrib.auth.hashers import make_password   # 密码加密模块

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email
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
                if user.is_active:
                    login(request, user)  # 登陆  login是django提供的登陆方法  user信息会放到request里 传到页面
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'username': user_name})
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


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()  # 实例化form
        return render(request, 'register.html', {'register_form': register_form})   # 将form对象传送到前端 这个对象里有验证码图片 需要在前端输出register_form.captcha

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 校验
        if register_form.is_valid():    # 如果校验通过
            user_name = request.POST.get('email', '')  # 获取用户名
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户名已被注册'})
            pass_word = request.POST.get('password', '')  # 获取密码
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)    # 对密码进行加密存储
            user_profile.is_active = False
            user_profile.save()     # 保存到数据库

            send_register_email(user_name, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
    def get(self, request, active_code):
        email_table = EmailVerifyRecord.objects.filter(code=active_code)    # filter返回的是一个类的集合
        if email_table:
            for each in email_table:
                user_table = UserProfile.objects.get(username=each.email)   # get返回一个类 如果查询到多个结果会报错
                if user_table:
                    user_table.is_active = True     # 修改为True 表示激活成功
                    user_table.save()
                else:
                    return render(request, 'register.html')
        else:
            return render(request, 'register.html', {'msg': '激活链接失效'})
        return render(request, 'login.html')


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()  # 实例化form
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})   # 将form对象传送到前端 这个对象里有验证码图片 需要在前端输出register_form.captcha

    def post(self, request):
        forget_form = ForgetForm(request.POST)  # 校验
        if forget_form.is_valid():    # 如果校验通过
            user_name = request.POST.get('email', '')  # 获取用户名
            if not UserProfile.objects.filter(username=user_name):
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '用户名不存在'})
            send_register_email(user_name, 'forget')
            return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '重置链接发送成功'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        email_table = EmailVerifyRecord.objects.filter(code=active_code)    # filter返回的是一个类的集合
        if email_table:
            for each in email_table:
                user_table = UserProfile.objects.get(username=each.email)   # get返回一个类 如果查询到多个结果会报错
                if user_table:
                    return render(request, 'password_reset.html', {'email': each.email})
                else:
                    return render(request, 'forgetpwd.html', {'msg': '重置密码链接失效'})
        else:
            return render(request, 'forgetpwd.html', {'msg': '重置密码链接失效'})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('email', '')
        if modify_form.is_valid():
            pwd = request.POST.get('password', '')
            pwd1 = request.POST.get('password1', '')
            if pwd != pwd1:
                return render(request, 'password_reset.html', {'msg': '两次输入的密码不一致', 'email': email})
            else:
                user = UserProfile.objects.get(email=email)
                password = make_password(pwd)
                user.password = password
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'modify_form': modify_form,  'email': email})
