from django.urls import path
from . import views
from . import course_views, staff_views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'cms'
urlpatterns = [
    path('index/', views.index, name='index'),

    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('write_news/', views.CMSView.as_view(), name='write_news'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_newses'),
    path('delete_news/', views.delete_news, name='delete_news'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_news_category/', views.NewsAddView.as_view(), name='add_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news'),
    path('delete_news_category/', views.delete_news_category, name='delete_news'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('qntoken/',views.qntoken,name='qntoken'),
    path('banners/', views.banner, name='banners'),
    path('add_banner/', views.add_banner, name='add_banners'),
    path('banner_list', views.banner_list, name='banner_list'),
    path('delete_banner', views.delete_banner, name='delete_banner'),
    path('edit_banner', views.edit_banner, name='edit_banner'),
]

# 课程相关url映射
urlpatterns += [
    path('pub_course/', course_views.PubCourseView.as_view(), name='pub_course'),
]

# 员工管理
urlpatterns += [
    path('staffs/', staff_views.staffs_view, name='staffs'),
    path('add_staff/', staff_views.AddStaffView.as_view(), name='add_staff'),
]