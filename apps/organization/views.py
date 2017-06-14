# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CityDict, CourseOrg
from .forms import UserAskForm
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


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)    # 实例化modelform
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)   # model form可以直接save 不用生成一个model然后再model.save()
            # HttpResponse返回特定的格式 content_type用来定义为json格式
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"输入错误"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页 展示机构的部分课程和部分讲师和机构介绍
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据机构列表页传过来的机构id 获取该机构信息
        # django的ORM提供了根据外键获取外键表信息 比如机构表有一个外键course 可以直接用course_set获取course表信息
        all_courses = course_org.course_set.all()[:3]   # 根据外键获取该机构的所有课程信息
        all_teachers = course_org.teacher_set.all()[:1]     # 根据外键获取该机构的所有教师信息
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'org_detail': 'home',
        })


class OrgCourseView(View):
    """
    机构课程 展示机构的所有课程
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据机构列表页传过来的机构id 获取该机构信息
        # django的ORM提供了根据外键获取外键表信息 比如机构表有一个外键course 可以直接用course_set获取course表信息
        all_courses = course_org.course_set.all()   # 根据外键获取该机构的所有课程信息
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'org_detail': 'course',
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据机构列表页传过来的机构id 获取该机构信息
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'org_detail': 'desc',
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据机构列表页传过来的机构id 获取该机构信息
        all_teachers = course_org.teacher_set.all()    # 根据外键获取该机构的所有教师信息
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers': all_teachers,
            'org_detail': 'teacher',
        })
