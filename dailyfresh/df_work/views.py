from django.shortcuts import render
from models import *

def anbaoxiang(request):
    worker = Worker.objects.filter(pk=1)[0]
    context = {
        'worker':worker,
    }
    return render(request,'df_work/anbaoxiang.html',context)
