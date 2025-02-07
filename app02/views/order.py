import random
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from app02 import models
from app02.utils.form import OrderModelForm
from app02.utils.pagination import Pagination


def order_list(request):
    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by("-id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "order_list.html", context)


def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：由后台生成
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S%f") + str(random.randint(1000, 9999))  # 内部生成订单号，并写到form中
        # 管理员：获取当前登录的管理员id
        form.instance.admin_id = request.session.get("info").get("id")  # 这个session信息需要在login的时候注入，否则为空
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)  # 直接传入dict，django会自动转json
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)
