#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from hashlib import sha1
from models import *
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo,OrderDetailInfo
from django.core.paginator import Paginator
import user_decorator


def register(request):
    context = {'title':'用户注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    #接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码是否一致
    if upwd != upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功转到登陆页面
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    #根据用户登陆名查询对象
    users = UserInfo.objects.filter(uname=uname)
    print uname
    #判断：如果未查到用户名错。判断密码是否正确
    if len(users)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    if goods_ids == '':
        goods_list = []
    else:
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context ={
        'title':'用户中心','page_name':1,
        'user_email':user_email,
        'user_name':request.session['user_name'],
        'goods_list':goods_list,
    }
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request,pindex):
    uid = request.session['user_id']
    order_info = OrderInfo.objects.filter(user_id=int(uid)).order_by('-oid')
    order_list = []
    for order in order_info:
        order_details = []
        details = order.orderdetailinfo_set.order_by('id')[:]
        detail_goods = []
        for detail in details:
            goods=[]
            good = GoodsInfo.objects.filter(id=int(detail.goods_id))[0]
            gtitle = good.gtitle
            gunit = good.gunit
            gpic = good.gpic
            dcount = detail.count
            dprice = detail.price
            goods.append(gtitle)
            goods.append(gunit)
            goods.append(gpic)
            goods.append(dcount)
            goods.append(dprice)
            detail_goods.append(goods)
        order_details.append(order)
        order_details.append(detail_goods)
        order_list.append(order_details)

    paginator = Paginator(order_list, 2)
    page = paginator.page(int(pindex))
    context = {
        'title':'用户中心','page_name':1,
        'page':page,'paginator':paginator,
    }
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'tilte':'用户中心','page_name':1,'user':user}
    return render(request,'df_user/user_center_site.html',context)

