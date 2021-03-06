from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.xfzauth.forms import LoginForm, RegisterForm
from apps.xfzauth.models import User
from utils import restful
from utils.captcha.xfzcaptcha import Captcha  # 验证码
from io import BytesIO  # 读写io操作
from utils.aliyunsdk.aliyunsms import send_sms


class LoginView(View):
    # 用户登陆
    def get(self, request):
        # 展示登陆页面
        pass
    def post(self, request):
        # 用户登陆验证
        form = LoginForm(request.POST)
        # 表单验证
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            # 调用django验证方法，验证用户
            user = authenticate(request, username=telephone, password=password)
            # 验证用户
            if user:
                # 是否激活
                if user.is_active:
                    login(request, user)
                    if remember:
                        # 设置session
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    return restful.ok()
                else:
                    return restful.unauth(message='权限不足')
            else:
                return restful.params_error(message='手机号或密码错误')
        else:
            errors = form.get_errors()
            return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

# 生成图形验证码
def img_captcha(request):
    # 生成图形验证码和文本
    text, image = Captcha.gene_code()
    # BytesIO相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将image对象存储到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针位置移动到最开始的位置（指针写入后会被移动到文件最末端）
    out.seek(0)
    # 创建响应对象
    response = HttpResponse(content_type='image/png')
    # 从BytesIO管道中，读取图片数据，保存到response对象上
    response.write(out.read())
    # 获取文件长度，out.tell()文件读取后指针移动到尾部，获取指针长度就是文件的大小
    response['Content-length'] = out.tell()
    # 将验证码存储在memcache中(小写，过期时间)
    cache.set(text.lower(), text.lower(), 5*60)
    return response


# 发送短信验证码
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    # result = send_sms(telephone,code)  # 调用发送短信短信任务
    # print(result)
    print(code)
    return restful.ok()

def cache_test(request):
    # 读取缓存
    cache.set('username', 'zhiliao', 60)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')

class Register(View):
    # 注册
    def post(self, request):
        # 表单验证
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 读取表单数据
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 创建用户
            user = User.objects.create_user(username=username, password=password, telephone=telephone)
            login(request, user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())
