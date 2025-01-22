from django import forms
from django.shortcuts import render, HttpResponse, redirect
from app02 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from app02.utils.pagination import Pagination


def index(request):
    return render(request, "index.html")


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {"n0": queryset})


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


def user_list(request):
    """ 用户列表 """
    queryset = models.Userinfo.objects.all()
    return render(request, "user_list.html", {"n0": queryset})


def user_add(request):
    """ 添加用户（原始方法） """
    if request.method == 'GET':
        context = {
            "gender_choices": models.Userinfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    # 获取用户提交的数据
    name = request.POST.get('name')
    password = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    creat_time = request.POST.get('creat_time')
    gender_id = request.POST.get('gender_id')
    depart_id = request.POST.get('depart_id')
    print(name, password, age, account, creat_time, gender_id, depart_id)
    if name and password and creat_time:
        models.Userinfo.objects.create(name=name, password=password, age=age,
                                       account=account, create_time=creat_time,
                                       gender=gender_id, depart_id=depart_id)
    else:
        return render(request, "user_add.html")
    return redirect("/user/list")


# ################# ModelForm 示例 ###################

class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.Userinfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # 方法1
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        # }

    # 方法2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            # 判断field是否为DateTimeField类型
            if isinstance(field, forms.DateTimeField):
                field.widget = forms.DateInput(attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": field.label,
                })
            # 判断field是否为DateField类型
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(attrs={
                    "type": "date",
                    "class": "form-control",
                    "placeholder": field.label,
                })


def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    user_obj = models.Userinfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=user_obj)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=user_obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/user/list")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """ 用户删除 """
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect("/user/list")


class PrettyModelForm(forms.ModelForm):
    # 验证方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误"), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = "__all__"  # 所有字段
        # exclude = ['level']  # 排除该字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            # 判断field是否为DateTimeField类型
            if isinstance(field, forms.DateTimeField):
                field.widget = forms.DateInput(attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": field.label,
                })
            # 判断field是否为DateField类型
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(attrs={
                    "type": "date",
                    "class": "form-control",
                    "placeholder": field.label,
                })

    # # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # 当编辑模式时，排除当前编辑的ID：self.instance.pk（添加模式，该值为None）
        # 验证手机号是否重复
        exists: bool = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyEditModelForm(PrettyModelForm):
    # 禁用字段方法1
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = "__all__"  # 所有字段
        # 禁用字段方法2
        # exclude = ['mobile']  # 排除该字段


def pretty_list(request):
    """ 靓号列表 """
    data_dict = {}
    search_data = request.GET.get("q", "")  # 有值传值，没值传空
    if search_data:
        data_dict["mobile__contains"] = search_data  # __contains：指mobile的值包含变量search_data的字符串，即可搜出

    # select * from 表 order by level desc;【Django中：-id是desc, id是asc】
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "n0": search_data,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """ 添加靓号 """
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # 用户POST提交数据，数据校验。
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """ 编辑用户 """
    obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=obj)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/pretty/list")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    """ 用户删除 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list")
