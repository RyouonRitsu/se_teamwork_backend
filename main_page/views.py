from django.shortcuts import render
from account.views import *
from book.views import *
from movie.views import *

# Create your views here.

"""
調用方法:
    前端發送GET或POST請求到/main_page/函數名, 並添加相應的Params或Body(data使用鍵值對形式), 即可獲得包含相應信息的響應返回
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
    961:    影视名过长
    962:    影视形式过长
    963:    影视类型过长
    964:    地区过长
    965:    上映日期不合法
    966:    导演名过长
    967:    编剧名过长
    968:    主演名过长
    969:    语言过长
    970:    片长不合法
    971:    影视不存在
    980:    关键词不能为空
"""


@csrf_exempt
def search(request):
    """
    全局模糊搜索功能, 每個關鍵字之間使用','分隔, 可以搜索用户, 书籍, 影视, 话题, 小组, 若不指定搜索类型, 则默认搜索所有信息, 类型之间也使用','分隔\n
    **可选** 根据关键字排序和选择升序降序(是否反转)\n
    只接受GET請求, Params格式為:\n
    ?keyword=value1[,value2,...][&type=类型][&sort_by=屬性名&reverse=(True or False)]

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method != 'GET':
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})
    keyword = request.GET.get('keyword')
    type_ = request.GET.get('type')
    if not keyword:
        return JsonResponse({'errno': 980, 'msg': '关键词不能为空'})
    data = {'用户': None, '书籍': None, '影视': None, '话题': None, '小组': None}
    if not type_:
        data['用户'] = get_user_info(request, raw=True)
        data['书籍'] = get_book_info(request, raw=True)
        data['影视'] = get_movie_info(request, raw=True)
        # 索同学请在这里实现你的模糊搜索函数
        # data['话题'] = get_topic_info(request, raw=True)
        # data['小组'] = get_group_info(request, raw=True)
    else:
        types = str(type_).split(',')
        if '用户' in types:
            data['用户'] = get_user_info(request, raw=True)
        if '书籍' in types:
            data['书籍'] = get_book_info(request, raw=True)
        if '影视' in types:
            data['影视'] = get_movie_info(request, raw=True)
        # 索同学请在这里实现你的模糊搜索函数
        # if '话题' in types:
        #     data['话题'] = get_topic_info(request, raw=True)
        # if '小组' in types:
        #     data['小组'] = get_group_info(request, raw=True)
    return JsonResponse({'errno': 0, 'msg': 'ok', 'data': data})
