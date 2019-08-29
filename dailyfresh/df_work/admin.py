from django.contrib import admin
from models import *

class WorkerAdmin(admin.ModelAdmin):
    list_display = ['id','wname','wchuohao','wsex','wshiji','wdanshen','whobby']

admin.site.register(Worker,WorkerAdmin)


