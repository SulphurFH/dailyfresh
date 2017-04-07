# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from df_user.islogin import islogin
from df_user.models import UserInfo
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from .models import *
from datetime import datetime
from decimal import Decimal
from django.db import transaction
# Create your views here.


@islogin
def order(request):
    uid = request.session.get('userid')
    user = UserInfo.objects.get(id=uid)

    orderid = request.GET.getlist('orderid')
    orderlist = []

    for id in orderid:
        orderlist.append(CartInfo.objects.get(id=int(id)))

    # 判断用户手机号是否为空，分别做展示
    if user.ureceive_phone == '':
        ureceive_phone = ''
    else:
        ureceive_phone = user.ureceive_phone[0:4] + \
            '****' + user.ureceive_phone[-4:]

    context = {'title': '提交订单', 'page_name': 1, 'orderlist': orderlist,
               'user': user, 'ureceive_phone': ureceive_phone}
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
def addorder(request):
    tran_id = transaction.savepoint()

    post = request.POST
    orderlist = post.getlist('id[]')
    total = post.get('total')
    address = post.get('address')

    uid = request.session.get('userid')
    time = datetime.now()

    order = OrderInfo()
    order.oid = '%s%d' % (time.strftime('%Y%m%d%H%M%S'), uid)
    order.user_id = uid
    order.odate = time
    order.ototal = Decimal(total)

    order.oaddress = address
    order.save()

    for orderid in orderlist:
        cartinfo = CartInfo.objects.get(id=orderid)
        good = GoodsInfo.objects.get(cartinfo__id=cartinfo.id)

        print(int(good.gkucun) >= int(cartinfo.count))
        if int(good.gkucun) >= int(cartinfo.count):
            detailinfo = OrderDetailInfo()
            goodinfo = GoodsInfo.objects.get(cartinfo__id=orderid)

            detailinfo.goods_id = int(goodinfo.id)
            detailinfo.order_id = int(order.oid)
            detailinfo.price = Decimal(int(goodinfo.gprice))
            detailinfo.count = int(cartinfo.count)

            detailinfo.save()
            cartinfo.delete()
        else:
            transaction.savepoint_rollback(tran_id)
            return JsonResponse({'status': 2})
    return JsonResponse({'status': 1})
