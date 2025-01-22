from django.shortcuts import render, HttpResponse, redirect
from app01 import models


# Create your views here.
def index(request):
    return HttpResponse("开始")


def user_list(request):
    # app01目录下的templates寻找user_list.html(根据app的注册顺序（setting），逐一去他们的templates目录寻找)
    return render(request, "user_list.html")


def user_add(request):
    return render(request, "user_add.html")


def tql(request):
    datalist0 = "你好"
    datalist1 = [1, "yys", "123456789"]
    datalist2 = {'id': 2, 'name': 'hao', 'mobile': 135555555}
    datalist3 = [{'id': 3, 'name': 'qqs', 'mobile': 1888888888}, ]

    return render(request, "tql.html", {"n0": datalist0, "n1": datalist1, "n2": datalist2, "n3": datalist3})


def news(req):
    # 1.定义一些新闻(字典或者列表)  或 去数据库 网络请求去联通新闻
    # 向地址:http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2024/11/news 发送请求,获取数据
    # 第三方模块:requests    (pip install requests)
    import requests
    res = requests.get("http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2024/11/news")
    res = res.json()
    print(res)

    return render(req, "news.html")


def something(request):
    # request是一个对象，封装了用户发送过来的所有请求相关数据

    # 1.获取请求方式 GET/POST
    print(request.method)

    # 2.在URL上传递值/something/?n1=123&n2=999
    print(request.GET)

    # 3.在请求体中提交数据
    print(request.POST)

    # 4.【响应】HttpResponse("返回内容")，内容字符串内容返回给请求者
    # return HttpResponse("something")

    # 5.【响应】读取HTML的内容 + 渲染(替换) -> 字符串，返回给用户浏览器。
    # return render(request, "something.html", {"tittle": "一些请求：看python终端打印"})

    # 6.【响应】浏览器重定向到其他页面
    return redirect("https://www.baidu.com")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # print(request.POST)
        username = request.POST.get("user")
        password = request.POST.get("pwd")

        if username == 'root' and password == '123':
            return HttpResponse("登录成功")
        else:
            return render(request, "login.html", {"n0": "登录失败"})


def orm(request):
    # 新建
    # models.Department.objects.create(title="销售部")
    # models.Department.objects.create(title="IT部")
    # models.Department.objects.create(title="运营部")

    # models.Userinfo.objects.create(name="wypeig", password="123", age=19)
    # models.Userinfo.objects.create(name="sad", password="123", age=19)
    # models.Userinfo.objects.create(name="asdasd", password="123", age=19)

    # 删除
    # models.Userinfo.objects.filter(id=3).delete()
    # models.Department.objects.all().delete()

    # 获取数据
    # data_list = [对象, 对象, ]
    # data_list = models.Userinfo.objects.all()

    # 获取第一个对象
    # models.Userinfo.objects.filter(id=1).first()

    # for obj in data_list:
    #     print(obj.id, obj.name, obj.password, obj.age)

    # 更新
    models.Userinfo.objects.filter(id=1).update(password=999)
    models.Userinfo.objects.filter(name="sad").update(password=9213412399)

    return HttpResponse("成功")


def info_list(request):
    # 1.获取数据库中所有的用户信息
    # [对象, 对象, 对象, ]
    user_list2 = models.Userinfo.objects.all()
    # user_list1 = models.Userinfo.objects.all().values()
    # user_key = models.Userinfo.objects.all().values().first().keys()

    return render(request, "info_list.html", {"n0": user_list2})


def info_add(request):
    if request.method == 'GET':
        return render(request, "info_add.html")

    # 获取用户提交的数据
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")

    if user and pwd and age:
        # 添加到数据库
        models.Userinfo.objects.create(name=user, password=pwd, age=age)
        return redirect("/info/list")
    return render(request, "info_add.html", {"n0": "添加失败"})


def info_delete(request):
    nid = request.GET.get("nid")
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect("/info/list")
