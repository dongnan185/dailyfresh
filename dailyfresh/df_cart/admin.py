from django.contrib import admin
from models import *

class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['user','goods','count']

admin.site.register(CartInfo,CartInfoAdmin)