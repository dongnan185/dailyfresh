#coding=utf-8
from django.http import HttpResponseRedirect
#如果未登陆转到登陆页面
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            read = HttpResponseRedirect('/user/login/')
            read.set_cookie('url',request.get_full_path())
            return read
    return login_fun