"""
修饰forms表单在HTML的呈现形式，以适配BootStrap的css
"""

from django import forms


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了Bootstrap的form-control类，使其具有 Bootstrap 样式。
        # Django 自动 将 models.CharField 的 verbose_name 映射 为 forms.CharField 的 label
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
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