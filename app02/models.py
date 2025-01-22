from django.db import models


class Department(models.Model):
    name = models.CharField(verbose_name="部门名称", max_length=16)

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    name = models.CharField(verbose_name="名称", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.SmallIntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)  # 整数位8(10-2)，小数位2
    create_time = models.DateField(verbose_name="入职时间")
    # 在django中做的约束
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    # 2. django自动
    #   - 写的depart
    #   - 生成mysql的数据列 depart_id
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    # insert into app02_userinfo(name,password,age,account,create_time,gender,depart_id) values("chi",123456,18,200,"2023-04-03",1,1);


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)  # 用char原因是后面方便正则表达式搜索，如果用int还得转str
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    level_choices = {
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    }
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)
    status_choices = {
        (1, "未占用"),
        (2, "已占用"),
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
