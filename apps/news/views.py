from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from apps.news.models import News, NewsCategory, Comment
from apps.xfzauth.decorators import xfz_login_required
from utils import restful
from xfz import settings
from .serializers import NewsSerializers, CommentSerializer
from .forms import PublicCommentForm

def index(request):
    newses = News.objects.all()
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories
    }
    return render(request, 'news/index.html', context=context)

def news_list(request):
    page = int(request.GET.get('p', 1))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    newses = News.objects.order_by('-pub_time')[start:end]
    serializer = NewsSerializers(newses, many=True)
    data = serializer.data
    return restful.result(data=data)

def news_detail(request,news_id):
    try:
        # news = News.objects.select_related('category','author').prefetch_related("comments__author").get(pk=news_id)
        news = News.objects.get(id=news_id)
        context = {
            'news': news
        }
        return render(request,'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404

@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serializer =  CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())

def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context['newses'] = newses
    return render(request, 'search/search.html', context=context)