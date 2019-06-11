from rest_framework import serializers

from apps.news.models import News, NewsCategory
from apps.xfzauth.serializers import UserSeralizers


class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']

class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSeralizers()
    class Meta:
        model = News
        fields = ['id', 'title', 'desc', 'thumbnail', 'category', 'author']