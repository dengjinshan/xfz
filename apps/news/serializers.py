from rest_framework import serializers

from apps.news.models import News, NewsCategory, Comment, Banner
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

class CommentSerializer(serializers.ModelSerializer):
    author = UserSeralizers()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'pub_time', 'author']

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'link_to', 'priority')