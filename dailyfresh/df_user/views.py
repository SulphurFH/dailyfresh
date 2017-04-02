# coding=utf-8
from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.


def register(request):
    context = {'title': '注册'}
    return render(request, 'df_user/register.html', context)


def user_exist(request):
    get = request.GET
    uname = get['uname']
    user = UserInfo.objects.filter(uname=uname).count()
    if user:
        data = {'status': 3}
    else:
        data = {'status': 1}
    return JsonResponse(data)


def email_exist(request):
    get = request.GET
    uemail = get['email']
    user = UserInfo.objects.filter(uemail=uemail).count()
    if user:
        data = {'status': 3}
    else:
        data = {'status': 1}
    return JsonResponse(data)


def user_handle(request):
    """用户注册验证及保存"""
    # 从request中获取POST提交信息
    post = request.POST
    uname = post['user_name']
    print(uname)
    upwd = post['pwd']
    ucpwd = post['cpwd']
    uemail = post['email']
    print(uemail)

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
    """用户登录页面"""
    uname = request.COOKIES.get('uname', '')
    context = {'title': '登录', 'uname': uname, 'user_error': 0}
    return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


def login_handle(request):
    """用户登录验证"""

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

        redir = HttpResponseRedirect('/user/user_center_info/')
        if remember != 0:
            redir.set_cookie('uname', uname)
        else:
            redir.set_cookie('uname', '', max_age=-1)

        # 验证通过,添加session信息
        request.session['uname'] = uname
        # 用户关闭浏览器session失效
        request.session.set_expiry(0)

        return redir
    else:
        context = {'uname': uname, 'upwd': upwd,
                   'user_error': 2, 'title': '登录'}
        return render(request, 'df_user/login.html', context)


def user_center_info(request):
    """用户登录成功首页"""

    uname = request.session.get('uname')
    if uname:
        user = UserInfo.objects.get(uname=uname)
        context = {'isLogin': True, 'title': '用户中心',
                   'uname': uname, 'ureceive_user': user.ureceive_user,
                   'uaddress': user.uaddress,
                   'ureceive_phone': user.ureceive_phone}
        return render(request, 'df_user/user_center_info.html', context)
    else:
        return redirect('/user/login/')


def user_center_site(request):
    uname = request.session.get('uname')
    if uname:
        user = UserInfo.objects.get(uname=uname)

        if request.method == 'POST':
            post = request.POST
            user.ureceive_user = post['ureceive_user']
            user.ureceive_phone = post['ureceive_phone']
            user.uaddress = post['uaddress']
            user.postcode = post['postcode']
            user.save()

        if user.ureceive_phone == '':
            ureceive_phone = ''
        else:
            ureceive_phone = user.ureceive_phone[0:4] + \
                '****' + user.ureceive_phone[-4:]
        context = {'isLogin': True, 'title': '用户中心',
                   'uname': uname, 'ureceive_phone': ureceive_phone,
                   'user': user}
        return render(request, 'df_user/user_center_site.html', context)
    else:
        return redirect('/user/login/')
