import hashlib
import hmac
import os
import time
from django import http
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from apps.course.models import Course, CourseOrder
from apps.xfzauth.decorators import xfz_login_required
from utils import restful
from xfz import settings


def course_index(request):
    # 新闻首页
    context = {
        'course': Course.objects.all()
    }
    return render(request, 'course/course_index.html', context)


def course_detail(request, course_id):
    # 新闻详情
    try:
        course = Course.objects.get(pk=course_id)
        buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
    except Course.DoesNotExist:
        return http.JsonResponse({'code': 400, 'errmsg': '查询错误'})

    context = {
        'course': course,
        'buyed': buyed
    }
    print(context)
    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    # 生成token
    # video：是视频文件的完整链接
    file = request.GET.get('video')

    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id,buyer=request.user,status=2).exists():
        return restful.params_error(message='请先购买课程！')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})


@xfz_login_required
def course_order(request,course_id):
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course,buyer=request.user,status=1,amount=course.price)
    context = {
        'course': course,
        'order': order,
        # /course/notify_url/
        'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
        'return_url': request.build_absolute_uri(reverse('course:course_detail',kwargs={"course_id":course.pk}))
    }
    return render(request,'course/course_order.html',context=context)