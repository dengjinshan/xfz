from django.shortcuts import redirect

from utils import restful


def xfz_login_required(func):
    # 定义装饰器，判断请求是否为ajax
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='青登陆')
            else:
                return redirect('/')
    return wrapper