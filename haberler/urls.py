from django.contrib import admin
from django.urls import path
from .views import *

app_name = "haberler"

urlpatterns = [
    path('son-haberler', last_news, name="sonhaberler"),
    path('addnews', addnews, name="addnews"),
    path('<slug:slug>', news_list, name="news_list"),
    path('detay/<slug:slug>', news_detail, name="news_detail"),


]
