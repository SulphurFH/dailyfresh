
# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from df_user.models import UserView
from df_user.islogin import islogin
from df_cart.models import CartInfo
from haystack.views import SearchView

# Create your views here.


def index(request):
    """
    index函数负责查询页面中需要展示的商品内容，
    主要是每类最新的4种商品和3中点击率最高的商品，
    每类商品需要查询2次
    """

    # 查询每类商品最新的4个和点击率最高的3个
    fruit = GoodsInfo.objects.filter(gtype__id=1).order_by("-id")[:4]
    fruit2 = GoodsInfo.objects.filter(gtype__id=1).order_by("-gclick")[:3]
    fish = GoodsInfo.objects.filter(gtype__id=2).order_by("-id")[:4]
    fish2 = GoodsInfo.objects.filter(gtype__id=2).order_by("-gclick")[:3]
    meat = GoodsInfo.objects.filter(gtype__id=3).order_by("-id")[:4]
    meat2 = GoodsInfo.objects.filter(gtype__id=3).order_by("-gclick")[:3]
    egg = GoodsInfo.objects.filter(gtype__id=4).order_by("-id")[:4]
    egg2 = GoodsInfo.objects.filter(gtype__id=4).order_by("-gclick")[:3]
    vegetables = GoodsInfo.objects.filter(gtype__id=5).order_by("-id")[:4]
    vegetables2 = GoodsInfo.objects.filter(gtype__id=5).order_by("-gclick")[:3]
    frozen = GoodsInfo.objects.filter(gtype__id=6).order_by("-id")[:4]
    frozen2 = GoodsInfo.objects.filter(gtype__id=6).order_by("-gclick")[:3]
    count = CartInfo.objects.filter(
        user_id=request.session.get('userid')).count()
    # 构造上下文
    context = {'title': '首页', 'fruit': fruit, 'count': count,
               'fish': fish, 'meat': meat, 'egg': egg,
               'vegetables': vegetables, 'frozen': frozen,
               'fruit2': fruit2, 'fish2': fish2, 'meat2': meat2,
               'egg2': egg2, 'vegetables2': vegetables, 'frozen2': frozen,
               'guest_cart': 1}

    # 返回渲染模板
    return render(request, 'df_goods/index.html', context)


def detail(request, foodid):
    """
    detail函数负责展示商品详细页面，主要需要查询的地方有：
    当前商品对象，当前商品对象类型，最新的2个商品对象。
    以及每次请求本函数累加商品点击量。
    """

    # 获取当前商品，并将点击数+1
    good = GoodsInfo.objects.get(id=foodid)
    good.gclick += 1
    good.save()
    # 查询最新的两个商品
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    # 查询当前商品的类型
    goodtype = TypeInfo.objects.get(goodsinfo__id=foodid)

    count = CartInfo.objects.filter(
        user_id=request.session.get('userid')).count()
    # 构造上下文
    context = {'title': '商品详情', 'good': good, 'guest_cart': 1, 'count': count,
               'newgood': newgood, 'isDetail': True, 'goodtype': goodtype}

    # 查询用户id、用户浏览商品总数、用户目前在浏览的商品
    userid = request.session.get('userid')
    if userid:
        countView = UserView.objects.filter(uid__id=userid).count()
        view = UserView.objects.filter(uid__id=userid, gid__id=foodid)

        # 判断是否有重复数据
        if len(view) != 0:
            view.delete()
        view = UserView()
        view.uid_id = userid
        view.gid_id = foodid
        view.save()

        # 判读用户浏览商品是否超过总数显示
        if countView >= 10:
            UserView.objects.filter(uid__id=userid).order_by('id')[0].delete()

    # 返回渲染模板
    return render(request, 'df_goods/detail.html', context)

    # # 返回渲染模板
    # response = render(request, 'df_goods/detail.html', context)

    # # 将点击的商品id存入cookie中
    # goods_ids = request.COOKIES.get('goods_ids')
    # if goods_ids != '':
    #     goods_ids1 = goods_ids.split(',')
    #     if goods_ids1.count(foodid) >= 1:
    #         goods_ids1.remove(foodid)
    #     goods_ids1.insert(0, foodid)
    #     if len(goods_ids1) >= 6:
    #         del goods_ids1[5]
    #     goods_ids = ','.join(goods_ids1)
    # else:
    #     good_ids = int(foodid)

    # response.set('goods_ids', good_ids)
    # # 返回response对象
    # return response


def goodlist(request, typeid, selectid, pageid):
    """
    goodlist函数负责展示某类商品的信息。
    url中的参数依次代表
    typeid:商品类型id;selectid:查询条件id，1为根据id查询，2位根据价格查询，3位根据点击量查询
    """

    # 获取最新发布的商品
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    # 根据条件查询所有商品
    if selectid == '1':
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('-id')
    elif selectid == '2':
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('gprice')
    elif selectid == '3':
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('-gclick')
    # 分页
    paginator = Paginator(sumGoodList, 15)
    goodList = paginator.page(int(pageid))
    plist = paginator.page_range
    # 确定商品的类型
    goodtype = TypeInfo.objects.get(id=typeid)
    count = CartInfo.objects.filter(
        user_id=request.session.get('userid')).count()
    # 构造上下文
    context = {'title': '商品详情', 'count': count, 'list': 1,
               'guest_cart': 1, 'goodtype': goodtype,
               'newgood': newgood, 'goodList': goodList,
               'typeid': typeid, 'selectid': selectid,
               'plist': plist, 'pageid': int(pageid)}

    # 渲染返回结果
    return render(request, 'df_goods/list.html', context)
