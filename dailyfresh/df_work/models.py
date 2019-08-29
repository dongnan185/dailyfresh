from django.db import models
from tinymce.models import HTMLField

class Worker(models.Model):
    wname = models.CharField(max_length=20)
    wchuohao = models.CharField(max_length=20)
    wjianjie = HTMLField()
    wshiji = models.CharField(max_length=100)
    wsex  = models.IntegerField()
    wpic = models.ImageField(upload_to='df_work')
    whobby = models.CharField(max_length=100)
    wdanshen = models.BooleanField(default=True)


