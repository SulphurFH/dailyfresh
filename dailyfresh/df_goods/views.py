# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *

# Create your views here.


def index(request):
    uname = request.session.get('uname')
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
    context = {'title': '首页', 'uname': uname, 'fruit': fruit,
               'fish': fish, 'meat': meat, 'egg': egg,
               'vegetables': vegetables, 'frozen': frozen,
               'fruit2': fruit2, 'fish2': fish2, 'meat2': meat2,
               'egg2': egg2, 'vegetables2': vegetables, 'frozen2': frozen,
               'guest_cart': 1}
    if uname:
        context['isLogin'] = True
    else:
        context['isLogin'] = False
    return render(request, 'df_goods/index.html', context)


def detail(request, foodid):
    good = GoodsInfo.objects.get(id=foodid)
    good.gclick += 1
    good.save()
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    goodtype = TypeInfo.objects.get(goodsinfo__id=foodid)
    uname = request.session.get('uname')
    context = {'title': '商品详情', 'uname': uname,
               'good': good, 'guest_cart': 1,
               'newgood': newgood, 'isDetail': True, 'goodtype': goodtype}
    if uname:
        context['isLogin'] = True
    else:
        context['isLogin'] = False
    return render(request, 'df_goods/detail.html', context)


def goodlist(request, typeid, selectid, pageid):
    uname = request.session.get('uname')
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
    # 构造上下文
    context = {'title': '商品详情', 'uname': uname,
               'guest_cart': 1, 'goodtype': goodtype,
               'newgood': newgood, 'goodList': goodList,
               'typeid': typeid, 'selectid': selectid,
               'plist': plist, 'pageid': int(pageid)}
    # 判断是否登录
    if uname:
        context['isLogin'] = True
    else:
        context['isLogin'] = False
    # 渲染返回结果
    return render(request, 'df_goods/list.html', context)
