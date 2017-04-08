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
    """
    此函数用户给下订单页面展示数据
    接收购物车页面GET方法发过来的购物车中物品的id，构造购物车对象供订单使用
    """

    uid = request.session.get('userid')
    user = UserInfo.objects.get(id=uid)

    # 获取勾选的每一个订单对象，构造成list，作为上下文传入下单页面
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

    # 构造上下文
    context = {'title': '提交订单', 'page_name': 1, 'orderlist': orderlist,
               'user': user, 'ureceive_phone': ureceive_phone}

    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@islogin
def addorder(request):
    """
    下订单功能
    1）根据页面上AJAX传来的请求，依次将价格、地址、用户id、时间保存为一条订单数据，订单id由时间构建
    2）由order函数传的orderlist，由place_order.html页面的JS构造成数组传到本视图，重新getlist解析为列表
       作为订单详情页中购物车中的每个商品
    3）根据步骤2）中得到的详细商品列表，构造订单详细信息表，减去相应的库存数量
    4）步骤3）执行后删除购物车中的信息
    """

    # 设置事务点，发生异常后回滚到此处
    tran_id = transaction.savepoint()

    # 根据POST和session获取信息
    post = request.POST
    orderlist = post.getlist('id[]')
    total = post.get('total')
    address = post.get('address')
    uid = request.session.get('userid')
    time = datetime.now()

    # 创建订单表
    order = OrderInfo()
    order.oid = '%s%d' % (time.strftime('%Y%m%d%H%M%S'), uid)
    order.user_id = uid
    order.odate = time
    order.ototal = Decimal(total)
    order.oaddress = address
    order.save()

    # 遍历购物车中提交信息，创建订单详情表
    for orderid in orderlist:
        cartinfo = CartInfo.objects.get(id=orderid)
        good = GoodsInfo.objects.get(cartinfo__id=cartinfo.id)

        # 判断库存是否够
        if int(good.gkucun) >= int(cartinfo.count):
            # 库存够，移除购买数量并保存
            good.gkucun -= int(cartinfo.count)
            good.save()

            goodinfo = GoodsInfo.objects.get(cartinfo__id=orderid)

            # 创建订单详情表
            detailinfo = OrderDetailInfo()
            detailinfo.goods_id = int(goodinfo.id)
            detailinfo.order_id = int(order.oid)
            detailinfo.price = Decimal(int(goodinfo.gprice))
            detailinfo.count = int(cartinfo.count)
            detailinfo.save()

            # 循环删除购物车对象
            cartinfo.delete()
        else:
            # 库存不够出发事务回滚
            transaction.savepoint_rollback(tran_id)
            # 返回json供前台提示失败
            return JsonResponse({'status': 2})

    # 返回json供前台提示成功
    return JsonResponse({'status': 1})


@islogin
def pay(request, oid):
    """
    虚拟支付页面
    """

    # 获取订单对象并修改ispay值
    orderinfo = OrderInfo.objects.get(oid=oid)
    orderinfo.isPay = True
    orderinfo.save()

    # 构造上下文
    context = {'oid': oid}

    return render(request, 'df_order/pay.html', context)
