# Generated by Django 4.2.11 on 2025-01-10 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0003_alter_userinfo_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateField(verbose_name='入职时间'),
        ),
    ]
