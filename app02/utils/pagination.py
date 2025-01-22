"""
自定义的分页组件，使用方法：
# 在视图函数中：
def pretty_list(request):
    # 1、根据需求筛选数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")
    # 2、实例化分页对象
    page_obj = Pagination(request, queryset, "page")
    # 3、
    context = {
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()       # html页码
    }
    return render(request, "pretty_list.html", context)

# 在HTML页面中：
    {% for obj in queryset %}
        <tr>
            <td>{{ obj.xxx }}</td>
        </tr>
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""
from django.utils.safestring import mark_safe


class Pagination:

    def __init__(self, request, queryset, page_param="page", page_size=10, plus=2):
        """
        属性：
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/pretty/list?page=12
        :param plus: 显示当前页的前后页码按钮数量
        """
        # page = request.GET.get(page_param, 1)
        # if page.isdecimal():
        #     page = int(page)
        # else:
        #     page = 1

        if request.GET.get(page_param, 1):
            page = abs(int(request.GET.get("page", 1)))  # 取绝对值
        else:
            page = 1

        self.page = page
        self.page_size = page_size  # 每页显示10条数据
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        self.plus = plus
        # 数据总条数
        self.total_count = queryset.count()
        # 总页码(切片数量)
        self.total_page_count, div = divmod(self.total_count, self.page_size)
        if div:
            self.total_page_count += 1  # for循环：取前不取后，所以要补1

    def html(self):
        """
        :return: HTML若干个<li></li>的文本
        """
        # 计算出，显示当前页的前2页，后2页
        start_page = self.page - self.plus
        end_page = self.page + self.plus + 1
        # 判断语句：避免页码显示坍缩，保持至少（2 * plus + 1）的数量。
        if start_page >= self.total_page_count - 2 * self.plus:
            start_page = self.total_page_count - 2 * self.plus
        if end_page <= 2 * self.plus + 1:
            end_page = 2 * self.plus + 1 + 1

        """ 制作html页码 """
        page_str_list = []
        # 上一页
        if self.page > 1 + self.plus:
            ele = f'<li><a href="?page={1}"><span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span></a></li>'
            page_str_list.append(ele)
        # 中间页码
        for i in range(start_page, end_page):
            if 0 < i <= self.total_page_count:
                if i == self.page:
                    ele = f'<li class="active"><a href="?page={i}">{i}</a></li>'
                else:
                    ele = f'<li><a href="?page={i}">{i}</a></li>'
                page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count - self.plus:
            ele = f'<li><a href="?page={self.total_page_count}"><span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span></a></li>'
            page_str_list.append(ele)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中

        return page_string
