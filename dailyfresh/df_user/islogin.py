# coding=utf-8
from django.http import HttpResponseRedirect


def islogin(func):
    """
    根据session判断用户是否登录，并将查询到的uname传入视图函数
    """

    def wrappedfunc(request, *args, **kwargs):
        if request.session.get('uname'):
            return func(request, *args, **kwargs)
        else:
            redir = HttpResponseRedirect('/user/login/')
            redir.set_cookie('url', request.get_full_path())
            return redir
    return wrappedfunc
