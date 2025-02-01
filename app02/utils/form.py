"""
这是一些form表单的格式定义，负责管理form表单允许填写什么内容，填写内容的规范化格式
"""

from django import forms
from app02 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app02.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.Userinfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
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


class PrettyEditModelForm(BootStrapModelForm):
    # 禁用字段方法1
    # mobile = forms.CharField(disabled=True, label="手机号")
    class Meta:
        model = models.PrettyNum
        fields = "__all__"  # 所有字段
        # 禁用字段方法2
        # exclude = ['mobile']  # 排除该字段
