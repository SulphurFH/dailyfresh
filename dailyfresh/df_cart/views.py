# coding=utf-8
from django.shortcuts import render, redirect
from df_user.islogin import islogin
from django.http import JsonResponse
from .models import *
from df_user.models import UserInfo
from df_goods.models import GoodsInfo

# Create your views here.


@islogin
def cart(request):
    """
    此函数用来展示购物车页面
    """

    # 根据用户获得购物车对象
    userid = request.session.get('userid')
    usercart = CartInfo.objects.filter(user_id=userid)

    # 构造上下文
    context = {'usercart': usercart, 'title': '我的购物车', 'page_name': 1}

    # 返回购物车页面
    return render(request, 'df_cart/cart.html', context)


@islogin
def addcart(request, foodid, counts):
    """
    此函数作为商品添加至购物车接口
    可根据GET（立即购买）和AJAX（list页面加入购物车、detail页面加入购物车）请求做响应
    添加购物车前先检查是否有本条数据，如果存在，则在原来数据基础上的count字段做累加
    """

    # 根据用户对象获得购物车对象
    userid = request.session.get('userid')
    userCart = CartInfo.objects.filter(user_id=userid, goods_id=foodid)

    # 校验是否存在本条记录，如果不存在就新建，存在则累加count值
    if len(userCart) == 0:
        cart = CartInfo()
        cart.goods_id = int(foodid)
        cart.user_id = userid
        cart.count = int(counts)
        cart.save()
    else:
        userCart[0].count += int(counts)
        userCart[0].save()

    # 如果请求是AJAX，则返回此用户下购物车对象条数
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=userid).count()
        return JsonResponse({'count': count})
    # 非AJAX直接转跳至购物车详细页面
    else:
        return redirect('/cart/')


@islogin
def edit(request, goodid, count):
    """
    在购物车详细页面中点击新增或减少商品数量，会通过AJAX方式触发本函数
    根据新增、修改后的商品数量保存到库中
    """
    # 获取购物车对象
    cart = CartInfo.objects.get(id=goodid)
    cart.count = count
    cart.save()

    return JsonResponse({'status': 1})


@islogin
def delcart(request, goodid):
    """
    购物车详细页面中点击删除，会通过AJAX方式出发本函数
    根据相应的购物车中商品对象，删除本条购物车对象
    """

    # 根据AJAX中商品id，删除对应的购物车对象
    try:
        cart = CartInfo.objects.get(id=goodid)
        cart.delete()
        return JsonResponse({'status': 1})
    except Exception as error:
        return JsonResponse({'status': 2})
