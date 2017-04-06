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
    userid = request.session.get('userid')
    usercart = CartInfo.objects.filter(user_id=userid)

    context = {'usercart': usercart, 'title': '我的购物车'}
    return render(request, 'df_cart/cart.html', context)


@islogin
def addcart(request, foodid, counts):
    userid = request.session.get('userid')

    userCart = CartInfo.objects.filter(user_id=userid, goods_id=foodid)
    if len(userCart) == 0:
        cart = CartInfo()
        cart.goods_id = int(foodid)
        cart.user_id = userid
        cart.count = int(counts)
        cart.save()
    else:
        userCart[0].count += int(counts)
        userCart[0].save()
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=userid).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@islogin
def edit(request, goodid, count):
    userid = request.session.get('userid')
    cart = CartInfo.objects.get(id=goodid)
    cart.count = count
    cart.save()
    return JsonResponse({'status': 1})


@islogin
def delcart(request, goodid):
    try:
        cart = CartInfo.objects.get(id=goodid)
        cart.delete()
        return JsonResponse({'status': 1})
    except Exception as error:
        return JsonResponse({'status': 2})
