from django.contrib import admin
from models import *

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['uname','upwd','uemail','ushou','uaddress','uyoubian','uphone']

admin.site.register(UserInfo,UserInfoAdmin)
