from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import User
from movie.models import *
from datetime import date
from account.views import login_required

# Create your views here.

"""
調用方法:
    前端發送GET或POST請求到/movie/函數名, 並添加相應的Params或Body(data使用鍵值對形式), 即可獲得包含相應信息的響應返回
errno:
    0:      [成功]
    901:    请求方式错误, 只接受POST请求
    902:    两次输入的密码不一致
    903:    用户名不合法
    904:    用户名已存在
    905:    密码不合法
    906:    用户不存在
    907:    Email不合法
    908:    手机号码不合法
    909:    城市或地址不合法
    910:    原密码错误
    911:    必填字段为空
    912:    用户未登录
    913:    重复登录
    914:    密码错误
    915:    年龄不合法
    916:    请求方式错误, 只接受GET请求
    917:    用户未登录, 且未提供任何可供查询的字段
    931:    ISBN已存在
    932:    ISBN过长
    933:    书名过长
    934:    排序字段不存在
    935:    书籍类型过长
    936:    作者姓名过长
    937:    作者国籍过长
    938:    出版社名过长
    939:    出版日期不合法
    940:    价格不合法
    941:    评分不合法
    942:    书籍不存在
    943:    热门度不合法
    944:    页数不合法
    945:    您没有权限执行此操作
    946:    找不到符合条件的结果
"""

