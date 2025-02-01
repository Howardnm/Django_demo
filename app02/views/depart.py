"""
部门管理
模块：增删改查
"""

from django.shortcuts import render, HttpResponse, redirect
from app02 import models
from app02.utils.pagination import Pagination


def index(request):
    return render(request, "index.html")


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    page_obj = Pagination(request, queryset)
    context = {
        "n0": queryset,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        return render(request, "depart_add.html")

    depart_name = request.POST.get("depart_name")
    if depart_name:
        models.Department.objects.create(name=depart_name)
    return redirect("/depart/list")


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")


def depart_edit(request, nid):
    """ 编辑部门 """
    if request.method == "GET":
        depart = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"depart": depart})

    depart_name = request.POST.get("depart_name")
    if depart_name:
        models.Department.objects.filter(id=nid).update(name=depart_name)
    return redirect("/depart/list")
