from django import forms
from apps.forms import FormMixin
from apps.news.models import News


class EditNewsCategory(forms.Form, FormMixin):
    # 定义表单
    pk = forms.IntegerField(error_messages={'requires':'必须传入分类id'})
    name = forms.CharField(max_length=100)

class WriteNewsForm(forms.Form, FormMixin):
    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']
