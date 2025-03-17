# Generated by Django 4.2.19 on 2025-03-17 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0009_alter_prettynum_level_alter_prettynum_status_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('img', models.CharField(max_length=128, verbose_name='头像')),
            ],
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='level',
            field=models.SmallIntegerField(choices=[(3, '3级'), (2, '2级'), (4, '4级'), (1, '1级')], default=1, verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '未占用'), (2, '已占用')], default=1, verbose_name='状态'),
        ),
    ]
