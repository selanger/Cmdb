## 自定义过滤器
from django import template
register = template.Library()
import time


@register.filter
def get_time(value):
    print(value)
    result = value.strftime("%Y-%m-%d %H:%M:%S")
    return result




