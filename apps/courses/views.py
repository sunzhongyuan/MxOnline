# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, Lesson
from operation.models import UserFavorite

# Create your views here.


class CourseView(View):
    def get(self, request):
        course_all = Course.objects.all()

        # 热门课程
        course_hot = course_all.order_by('-fav_nums')[:3]

        # 排序 最热门
        sort = request.GET.get('sort', '')
        if sort == 'students':
            course_all = course_all.order_by('-students')
        elif sort == 'hot':
            course_all = course_all.order_by('-click_nums')
        else:
            course_all = course_all.order_by('-add_time')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_all, 4, request=request)

        course_all = p.page(page)

        return render(request, 'course-list.html', {
            'course_all': course_all,
            'course_hot': course_hot,
            'sort': sort,
            'type': 'course',
        })


class CourseDescView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 相关课程 根据标签查找相关课程
        if course.tag:
            relate_course = Course.objects.filter(tag=course.tag)[:3]
        else:
            relate_course = []

        course_fav = False
        org_fav = False
        # 如果用户登录了 判断这个用户是否收藏了这个课程 或者 机构
        if request.user.is_authenticated():
            # 课程是否收藏
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                course_fav = True

            # 机构是否收藏
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                org_fav = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'type': 'course',
            'course_fav': course_fav,
            'org_fav': org_fav,

        })
