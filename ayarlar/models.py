from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import os


class SiteSettings(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    domain = models.CharField(max_length=70)
    logo = models.ImageField(upload_to="site")
    logo_nav = models.ImageField(upload_to="site")
    icon = models.ImageField(upload_to="site")
    keywords = models.CharField(max_length=150)
    post_detail = models.SmallIntegerField(help_text="Haber detayında sayfa başına düşen karakter sayısı örn:1000",
                                           verbose_name="Haber Detay Karakter", default=1000)
    page_size = models.SmallIntegerField(help_text="Sayfa başına düşen haber sayısı",verbose_name="Haber Sayısı",default=5)
    facebook = models.CharField(max_length=100, default="0")
    twitter = models.CharField(max_length=100, default="0")
    instagram = models.CharField(max_length=100, default="0")
    linkedin = models.CharField(max_length=100, default="0")
    pinterest = models.CharField(max_length=100, default="0")
    youtube = models.CharField(max_length=100, default="0")
    google_plus = models.CharField(max_length=100, default="0")
    tumblr = models.CharField(max_length=100, default="0")
    footer_text = models.CharField(max_length=250)
    top_banner = models.ImageField(upload_to="site", null=True, blank=True)
    iyzi_api = models.CharField(max_length=250,verbose_name="İyzi api key",help_text="İyzico api key")
    iyzi_secret_key = models.CharField(max_length=250,verbose_name="İyzico secret key",help_text="İyzico secret key")

    def __str__(self):
        return self.title

    def f(instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            return '{}.{}'.format(instance.pk, ext)
        else:
            pass



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(blank=True, upload_to="user")
    facebook = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    pinterest = models.CharField(max_length=100)
    google_plus = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
