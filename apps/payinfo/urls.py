from django.urls import path
from  . import views

app_name = 'payinfo'
urlpatterns = [
    path('', views.index, name='index'),
    path('doenload/', views.download, name='download'),
    path('payinfo_order/', views.payinfo_order, name='payinfo_order'),
    path('notify_view/', views.notify_view, name='notify_view'),
]