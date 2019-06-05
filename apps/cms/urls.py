from django.urls import path
from . import views


app_name = 'cms'
urlpatterns = [
    path('login/', views.CmsView.as_view(), name='login'),
]