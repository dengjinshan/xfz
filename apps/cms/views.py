from django.shortcuts import render
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST

from apps.cms.forms import EditNewsCategory, WriteNewsForm
from apps.news.models import NewsCategory, News
from utils import restful
import os
from django.conf import settings


@staff_member_required(login_url='')
def index(request):
    return render(request, 'cms/index.html')


class CMSView(View):
    # 后台管理
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = form.cleaned_data.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail,
                                content=content, category=category, author=request.POST)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)

class NewsAddView(View):
    # 添加新闻
    def post(self, request):
        name = request.POST.get('name')
        exists = NewsCategory.objects.filter(name=name).exists()
        if not exists:
            NewsCategory.objects.create(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='分类已存在')

@require_POST
def edit_news_category(request):
    # 获取反序列化对象
    forms = EditNewsCategory(request.POST)
    # 验证
    if forms.is_valid():
        pk = forms.cleaned_data.get('pk')
        name = forms.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except Exception as e:
            return restful.params_error(message='改分类不存在')
    else:
        return restful.params_error(message=forms.get_errors())


@require_POST
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在！')

@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    # http://127.0.1:8000/media/abc.jpg
    return restful.result(data={'url':url})

