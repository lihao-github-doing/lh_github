import traceback
from itertools import chain

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from course.models import TCategory, TArticle


def index(request):
    username = request.COOKIES.get('username').encode('latin-1').decode('utf-8')
    # 初始化分类表
    cates = TCategory.objects.all()
    #初始化文章表
    art = TArticle.objects.all()
    ride = request.GET.get('ride')
    if ride == 'True':
        art = TArticle.objects.all().order_by('-count')
    rides = request.GET.get('ridee')
    if rides == 'True':
        artt = TArticle.objects.all().order_by('-publish_time')
    # 初始化分页器
    pagtor = Paginator(object_list=art,per_page=3)
    #接收number页数，用于跳转页面
    number = int(request.GET.get('number',1))
    #如果未传递number或number超出限制，跳转到第一页
    if number not in pagtor.page_range:
        number = 1
    #创建page对象
    page = pagtor.page(number)
    #传递cate和page对象
    return render(request,'course/index.html',{'page':page, 'cates':cates,'username':username})

def base(request):
    username = request.COOKIES.get('username').encode('latin-1').decode('utf-8')
    # 获取所有分类，用于侧边栏
    cates = TCategory.objects.all()
    # 获取类别id用于查询文章
    id = request.GET.get('id')
    number = int(request.GET.get('number', 1))
    level = int(request.GET.get('level'))
    if level == 2:
        article = TArticle.objects.filter(cate_id=id)
        pagtor = Paginator(object_list=article,per_page=3)
        if number not in pagtor.page_range:
            number = 1
        page = pagtor.page(number)
        na = TCategory.objects.get(pk=id)
        parent_name = TCategory.objects.get(pk=na.parent_id).title
        parent_id =TCategory.objects.get(pk=na.parent_id).id
        return render(request,'course/pythonBase.html',{'page':page,'cates':cates,'id':id,'level':level,'parentname':parent_name,'name':na.title,'parent_id':parent_id,'username':username})
    else:
        artt = TArticle.objects.filter(cate__parent_id=id)
        pagtor = Paginator(object_list=artt,per_page=3)
        if number not in pagtor.page_range:
            number = 1
        page = pagtor.page(number)
        name = TCategory.objects.get(pk=id).title
        return render(request,'course/pythonBase.html',{'page':page,'cates':cates,'id':id,'level':level,'name':name,'username':username})

# 删除
def delete(request):
    id = request.GET.get('id')
    number=request.GET.get('number')
    try:
        result = TArticle.objects.get(id=id)
        with transaction.atomic():
            result.delete()
            users=TArticle.objects.all()
            pagtor=Paginator(object_list=users,per_page=3)
            try:
                page=pagtor.page(number)
                return HttpResponse(number)
            except:
                return HttpResponse(int(number)-1)
    except:
        traceback.print_exc()
        return HttpResponse('删除失败')

# 添加课程
def add_course(request):
    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)
    return render(request,'course/addCourse.html',{'cates':cates,'sub_cates':sub_cates})

def add_course_logic(request):
    try:
        name=request.POST.get('title')
        level = int(request.POST.get('level'))
        sub_name = request.POST.get('cate_sel')
        print('课程',name,'级别',level,'分类',sub_name)
        with transaction.atomic():
            if sub_name:
                result = TCategory.objects.get(title=sub_name)
                TCategory.objects.create(title=name, level=2, parent_id=result.id)
            else:
                TCategory.objects.create(title=name, level=1)
        return redirect('course:index')
    except:
        traceback.print_exc()
        return HttpResponse('添加失败')

# 添加文章
def add_article(request):
    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)
    return render(request,'course/addArticle.html',{'cates':cates,'sub_cates':sub_cates,})

def add_article_logic(request):
    try:
        name=request.POST.get('article_name')  #文章名
        cate_id=request.POST.get("course_sel")  # 分类
        sub_cate_id=request.POST.get('cate_sel')  # 课程
        publishTime=request.POST.get('publishtime') #发布时间
        content=request.POST.get('content') #内容
        print('文章名',name,'一级分类id',cate_id,'二级分类id',sub_cate_id,'添加时间',publishTime,'内容',content)
        with transaction.atomic():
            TArticle.objects.create(title=name,count=0,cate_id=sub_cate_id,publish_time=publishTime,content=content)
            return redirect('course:index')
    except:
        traceback.print_exc()
        return HttpResponse('添加失败')

def get_category(request):
    course_id = request.GET.get("course_id")
    cates = TCategory.objects.filter(parent_id=course_id)
    def my_default(c):
        if isinstance(c, TCategory):
            return {"id": c.id, "title": c.title}
    return JsonResponse(list(cates), safe=False, json_dumps_params={"default": my_default})

# 修改文章
def update(request):
    try:
        id = request.GET.get('id')
        article = TArticle.objects.get(id=id)  # 文章
        sub_cate = TCategory.objects.get(id=article.cate_id)
        parent_id = sub_cate.parent_id
        cate = TCategory.objects.filter(id=parent_id)
        cates = TCategory.objects.filter(level=1)      # 一级分类
        sub_cates = TCategory.objects.filter(level=2)  # 二级分类
        return render(request,'course/update.html',{'article':article,
                                                    'cates':cates,
                                                    'cate_id':cate[0].id,
                                                    'sub_cates':sub_cates,
                                                    })
    except:
        traceback.print_exc()
        return HttpResponse('跳转出错')

def update_logic(request):
    try:
        id=request.GET.get('id')
        article_name=request.POST.get('article_name')  #文章名称
        check_course=request.POST.get('course_sel')  # 一级分类名
        check_cate=request.POST.get('cate_sel')     # 二级分类名
        content=request.POST.get('input_text')   #文章内容
        print('id',id,'文章名',article_name,'课程id',check_course,'分类id',check_cate,'文章内容',content)
        with transaction.atomic():
            result=TArticle.objects.get(id=id)
            result.title=article_name
            result.course_id=check_cate
            result.content=content
            result.save()
            return redirect('course:index')
    except:
        traceback.print_exc()
        return HttpResponse('修改失败')