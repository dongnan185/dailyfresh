#coding=utf-8
from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal
from df_cart.models import CartInfo

@user_decorator.login
def order(request):
    #查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    #根据提交查询购物车信息
    get = request.GET
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)

    context = {
        'title':'提交订单','page_name':1,
        'user':user,'carts':carts,
        'cart_ids':','.join(cart_ids),
    }
    return render(request,'df_order/order.html',context)

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    #接受购物车编号
    cart_ids = request.POST.get('cart_ids')
    print '%s' %cart_ids;
    try:
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.id = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now

        order.ototal = Decimal(request.POST.get('total'))
        order.save()
        #创建订单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            #查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            #判断商品库存
            goods = cart.goods
            if goods.gkucun>cart.count:
                #减少商品库存
                goods.gkucun = cart.goods.gkucun - cart.count
                goods.save()
                #完善详细订单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                #删除购物车数据
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)

    except Exception as e:
        print '================%s'%e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')

@user_decorator.login
def pay(request,oid):
    order = OrderInfo.objects.get(oid=oid)
    order.IsPay = True
    order.save()
    context = {'order':order}
    return render(request,'df_order/pay.html',context)




