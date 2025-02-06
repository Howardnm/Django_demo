# django命令生成数据库表

```shell
# 每次修改完models.py，要执行以下命令同步到数据库
python manage.py makemigrations
python manage.py migrate
```

## django 指引
- setting.py
```python
# 添加app02的服务模块
INSTALLED_APPS += ['app02.apps.App02Config']

# 添加中间件，用于验证用户访问合法性
MIDDLEWARE += ['app02.middleware.auth.AuthMiddleware']

# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',  # 数据库名字
        'USER': 'root',
        'PASSWORD': '123456789',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

# 修改django的语言
LANGUAGE_CODE = 'zh-hans'
```

- 文件模块依赖关系
```text
models.py ---> /utils/form.py --> | ~~~~~~~~~~~~~ |
/utils/*.py(一些功能组件) --------> | /views/*.py   | --> urls.py
/static --> /templates/*.html --> | ~~~~~~~~~~~~~ |
```

- 中间件(/middleware/*.py)
```text
1、中间组件功能：
    可用于验证用户身份
2、应用中间件：(按列表顺序执行中间件)
    django 的 setting.py 添加：MIDDLEWARE += ['app02.middleware.auth.M1','app02.middleware.auth.M2',]
3、编写中间件函数：
    class M1(MiddlewareMixin):
        def process_request(self, request):
            return
        def process_response(self, request, response):
            return response
4、原理
    用户访问 --> process_request(M1)  --(返回None)--> process_request(M2) --(返回None)--> |~~~~~~~~~~~~~~~~~~~~|
                       |(有返回值）                          |(有返回值）                 | def index(request) |
    用户响应 <-- process_response(M1) <------------- process_response(M2) <------------ |~~~~~~~~~~~~~~~~~~~~|
```

