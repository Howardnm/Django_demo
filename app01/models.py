from django.db import models

# 以下django会帮你在mysql创建一个数据表，【id列】不写也会自动生成。
"""
create table app01_userinfo(
    id bigint auto_increment primary key,
    name varchar(32),
    password varchar(64),
    age int
)
"""


# Create your models here.
class Userinfo(models.Model):
    name = models.CharField(verbose_name="名称", max_length=32)  # verbose_name相当于注解
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.CharField(verbose_name="年龄", max_length=32)
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="创建时间")

    # 无约束
    # department_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束（数据库做的约束）
    #   - to="Department", 与这张表关联
    #   - to_field="id", 表中的这一列关联
    # 2. django自动
    #   - 写的depart
    #   - 生成mysql的数据列 depart_id
    # 3.部门表被删除
    # 3.1 级联删除
    # depart = models.ForeignKey(to="Department", to_field="id",on_delete=models.CASCADE)
    # 3.2 置空
    depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Department(models.Model):
    title = models.CharField(max_length=16)

# ########## 新建数据 ###########
# 本质:insert into app01_department(title) values("销售部”)
# Department.objects.create(title="销售部")
# Userinfo.objects.create(name="wypeig", password="123", age=19)
