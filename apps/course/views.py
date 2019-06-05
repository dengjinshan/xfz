from django.shortcuts import render

# Create your views here.

def course_index(request):
    # 新闻首页
    return render(request, 'course/course_index.html')

def course_detail(request, course_id):
    # 新闻详情
    return render(request, 'course/course_detail.html')

