from django.shortcuts import render
from django.views import View


class CmsView(View):
    def get(self, request):
        return render(request, 'cms/login.html')