from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'cms'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('write_news/', views.CMSView.as_view(), name='write_news'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_news_category/', views.NewsAddView.as_view(), name='add_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news'),
    path('delete_news_category/', views.delete_news_category, name='delete_news'),
    path('upload_file/', views.upload_file, name='upload_file'),
]