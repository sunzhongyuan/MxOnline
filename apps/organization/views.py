from django.shortcuts import render
from django.views.generic.base import View

from .models import CityDict, CourseOrg
# Create your views here.


class OrgView(View):
    def get(self, request):
        org_all = CourseOrg.objects.all()
        org_nums = org_all.count()
        city_all = CityDict.objects.all()
        return render(request, 'org-list.html', {
            'org_nums': org_nums,
            'org_all': org_all,
            'city_all': city_all
        })
