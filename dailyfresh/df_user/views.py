# coding=utf-8
from django.shortcuts import render, redirect
from .models import *
from df_goods.models import GoodsInfo
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
from .islogin import islogin

# Create your views here.


def register(request):
    """
    注册页面
    """

    context = {'title': '注册'}
    return render(request, 'df_user/register.html', context)


def user_exist(request):
    """
    前台js校验用户名是否存在的接口
    用户名已存在，返回status:3的json，用户名不存在，返回status:1的json
    """

    get = request.GET
    uname = get['uname']
    user = UserInfo.objects.filter(uname=uname).count()
    if user:
        data = {'status': 3}
    else:
        data = {'status': 1}
    return JsonResponse(data)


def email_exist(request):
    """
    前台js校验邮箱是否存在的接口
    邮箱已存在，返回status:3的json，邮箱不存在，返回status:1的json
    """

    get = request.GET
    uemail = get['email']
    user = UserInfo.objects.filter(uemail=uemail).count()
    if user:
        data = {'status': 3}
    else:
        data = {'status': 1}
    return JsonResponse(data)


def user_handle(request):
    """
    用户注册验证及保存
    从前台POST中得到uname、upwd、ucpwd、uemail
    针对两次密码进行校验是否一致，一致后进行加密存库
    """

    # 从request中获取POST提交信息
    post = request.POST
    uname = post['user_name']
    upwd = post['pwd']
    ucpwd = post['cpwd']
    uemail = post['email']

    # 校验两次提交的密码是否一致
    if upwd != ucpwd:
        return redirect('/user/register/')

    # 针对密码进行sha1加密
    upwd1 = sha1()
    upwd1.update(upwd)
    upwd_sha1 = upwd1.hexdigest()

    # 保存用户注册信息
    userinfo = UserInfo()
    userinfo.uname = uname
    userinfo.upwd = upwd_sha1
    userinfo.uemail = uemail
    userinfo.save()

    return redirect('/user/login/')


def login(request):
    """
    用户登录页面
    """

    uname = request.COOKIES.get('uname', '')
    context = {'title': '登录', 'uname': uname, 'user_error': 0}
    return render(request, 'df_user/login.html', context)


def logout(request):
    """
    用户退出，退出后清空session
    """

    # 清空会话数据
    request.session.flush()
    return redirect('/user/login/')


def login_handle(request):
    """
    用户登录验证
    根据POST表单传入的uname、upwd进行数据库里校验
    根据remember的值判断是否在cookie中存入uname
    验证成功后将uname和userid存入session
    """

    # 从request中获取POST提交信息
    post = request.POST
    uname = post['username']
    upwd = post['pwd']
    remember = post.get('remember', 0)

    user = UserInfo.objects.filter(uname=uname)

    if user:
        # 根据sha1加密后与数据库用户密码对比
        upwd1 = sha1()
        upwd1.update(upwd)
        upwd_sha1 = upwd1.hexdigest()

        # 验证密码是否正确
        if user[0].upwd != upwd_sha1:
            context = {'uname': uname, 'upwd': upwd,
                       'user_error': 1, 'title': '登录'}
            return render(request, 'df_user/login.html', context)

        url = request.COOKIES.get('url', '/')
        redir = HttpResponseRedirect(url)
        redir.set_cookie('url', '', max_age=-1)

        if remember != 0:
            redir.set_cookie('uname', uname)
        else:
            redir.set_cookie('uname', '', max_age=-1)

        # 验证通过,添加session信息
        request.session['uname'] = uname
        request.session['userid'] = user[0].id
        # 用户关闭浏览器session失效
        request.session.set_expiry(0)

        return redir
    else:
        context = {'uname': uname, 'upwd': upwd,
                   'user_error': 2, 'title': '登录'}
        return render(request, 'df_user/login.html', context)


@islogin
def user_center_info(request):
    """
    用户个人信息页面
    """

    # 判断用户是否登录，并传入上下文
    user = UserInfo.objects.get(uname=request.session.get('uname'))

    # 查询用户最近浏览的前5个商品
    goods = UserView.objects.filter(
        uid__id=request.session.get('userid')).order_by('-id')[:5]
    goodlist = []
    for good in goods:
        goodlist.append(GoodsInfo.objects.get(id=good.gid_id))

    # goodlist = []
    # goods_ids = request.COOKIES.get('goods_ids', '')
    # goods_ids1 = goods_ids.split(',')
    # if goods_ids1 != ['']:
    #     for goodid in goods_ids1:
    #         goodlist.append(GoodsInfo.objects.get(id=int(goodid)))
    context = {'title': '个人信息', 'info': 1,
               'ureceive_user': user.ureceive_user,
               'uaddress': user.uaddress, 'goodlist': goodlist,
               'ureceive_phone': user.ureceive_phone, 'page_name': 1}
    return render(request, 'df_user/user_center_info.html', context)


@islogin
def user_center_site(request):
    """
    用户信息设置页面
    根据用户请求此url的方式是GET or POST来做页面展示 or 数据保存
    """

    # 判断用户是否登录，并传入上下文
    user = UserInfo.objects.get(uname=request.session.get('uname'))

    # 获取用户输入POST信息
    if request.method == 'POST':
        post = request.POST
        user.ureceive_user = post['ureceive_user']
        user.ureceive_phone = post['ureceive_phone']
        user.uaddress = post['uaddress']
        user.postcode = post['postcode']
        user.save()

    # 判断用户手机号是否为空，分别做展示
    if user.ureceive_phone == '':
        ureceive_phone = ''
    else:
        ureceive_phone = user.ureceive_phone[0:4] + \
            '****' + user.ureceive_phone[-4:]

    # 构造上下文
    context = {'title': '收货地址', 'site': 1,
               'ureceive_phone': ureceive_phone,
               'user': user, 'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)


@islogin
def user_center_order(request):
    context = {'page_name': 1, 'title': '全部订单',
               'order': 1}
    return render(request, 'df_user/user_center_order.html', context)
