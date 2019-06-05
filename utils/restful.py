from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    paramserror = 400  # 参数
    unauth = 401  # 权限
    methoderror = 405  # 路径
    servererror = 500  # 服务器

def result(code=HttpCode.ok, message='', data=None, kwages=None):
    json_dict = {'code':code, 'message':message, 'data':data, }
    if kwages and isinstance(kwages,dict) and kwages.keys():
        json_dict.update(kwages)

    return JsonResponse(json_dict)

def ok():
    return result()

def params_error(message='', data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)

def unauth(message='', data=None):
    return result(code=HttpCode.unauth, message=message, data=data)

def method_error(message='', data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)

def server_error(message='', data=None):
    return result(code=HttpCode.servererror, message=message, data=data)