# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, Lesson

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
        # 获取章节数
        lesson_nums = course.lesson_set.all().count()
        # 获取学习用户
        stu = course.usercourse_set.all()

        return render(request, 'course-detail.html', {
            'course': course,
            'lesson_nums': lesson_nums,
            'stu': stu,
            'type': 'course',

        })
