import os

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app02 import models
from app02.utils.form import UpForm, UpModelForm


def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")
    # print(request.POST)  # 请求体中的数据
    # <QueryDict: {'csrfmiddlewaretoken': ['i5BzGvgiHYMGB5dUPvE5znnSThmH8Vig3mPKwWclmwNqkn5PbKAFgx3NukYo6p1d'], 'username': ['']}>
    # print(request.FILES)  # 请求发过来的文件
    # <MultiValueDict: {'avatar': [<InMemoryUploadedFile: 新建文本文档.txt (text/plain)>]}>

    file_obj = request.FILES.get("avatar")
    # print(file_obj.name)  # 取得文件名
    f = open(file_obj.name, mode="wb")
    for chunk in file_obj.chunks():  # file_obj.chunks 文件分块读取
        f.write(chunk)
    f.close()

    return render(request, "upload_list.html")


def upload_form(request):
    tittle = "form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "tittle": tittle})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        # {'name': 'asd', 'age': '23', 'img': <InMemoryUploadedFile: 456.png (image/png)>}
        # 1.读取图片内容，写入到文件夹中并获取文件的路径
        img_obj = form.cleaned_data.get("img")
        # file_path = "app02/static/img/{}".format(img_obj.name)
        db_file_path = os.path.join("static", "img", img_obj.name)  # 让数据库写入这个路径，方便套域名访问
        file_path = os.path.join("app02", "static", "img", img_obj.name)  # 用os写路径，避免操作系统分隔符问题，例如\/
        f = open(file_path, mode="wb")
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()

        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=db_file_path,
        )

        return render(request, "upload_form.html", {"form": form, "tittle": tittle})
    return render(request, "upload_form.html", {"form": form, "tittle": tittle})


def upload_modelform(request):
    tittle = "modelform上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html", {"form": form, "tittle": tittle})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保持
        # 字段、上传路径写入到数据库
        form.save()
        return render(request, "upload_form.html", {"form": form, "tittle": tittle})
    return render(request, "upload_form.html", {"form": form, "tittle": tittle})