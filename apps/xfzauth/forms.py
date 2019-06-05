from django import forms
from apps.forms import FormMixin

class LoginForm(forms.Form, FormMixin):
    # 定义验证表单，（类视序列化器
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=12, min_length=6)
    remember = forms.IntegerField(required=False)