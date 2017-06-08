# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CityDict, CourseOrg
# Create your views here.


class OrgView(View):
    def get(self, request):
        org_all = CourseOrg.objects.all()
        city_all = CityDict.objects.all()

        # 热门机构
        org_hot = org_all.order_by('-click_nums')[:3]

        # 筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            org_all = org_all.filter(city_id=int(city_id))

        # 筛选机构类别
        category = request.GET.get('ct', '')
        if category:
            org_all = org_all.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            org_all = org_all.order_by('-students')
        elif sort == 'courses':
            org_all = org_all.order_by('-courses')

        # 计算机构数量
        org_nums = org_all.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_all, 5, request=request)

        org_all = p.page(page)

        # 应答前端
        return render(request, 'org-list.html', {
            'org_nums': org_nums,
            'org_all': org_all,
            'city_all': city_all,
            'city_cur': city_id,
            'category': category,
            'sort': sort,
            'org_hot': org_hot,
        })

