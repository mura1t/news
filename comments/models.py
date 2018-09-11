from django.db import models
from haberler.models import News


class NewsComment(models.Model):
    parent = models.ForeignKey(News,on_delete=models.CASCADE,verbose_name="Haber")
    user = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    mail = models.CharField(max_length=80)
    active = models.BooleanField(default=False)
    web_site = models.CharField(max_length=50,null=True,blank=True)
