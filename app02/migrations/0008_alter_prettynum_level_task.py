# Generated by Django 4.2.11 on 2025-02-06 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0007_admin_alter_prettynum_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prettynum',
            name='level',
            field=models.SmallIntegerField(choices=[(1, '1级'), (4, '4级'), (2, '2级'), (3, '3级')], default=1, verbose_name='等级'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '一般')], default=2, verbose_name='级别')),
                ('tittle', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='任务详细信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.admin', verbose_name='负责人')),
            ],
        ),
    ]
