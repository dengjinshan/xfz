from django.shortcuts import render, redirect
from django.urls import reverse

from apps.xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group


def staffs_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs': staffs
    }
    return render(request, 'cms/staffs.html', context=context)

class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/add_staff.html', context=context)

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        user.is_staff = True
        group_ids = request.POST.getlist('groups')
        groups = Group.objects.filter(pk__in=group_ids)
        user.groups.set(groups)
        user.save()
        return redirect(reverse('cms:staffs'))
