from django import template
from haberler.models import News, NewsGallery

register = template.Library()
from haberler.models import Category,SubCategory
from django.core.cache import cache
from ayarlar.models import SiteSettings
from reklam.models import Reklam
import django_filters


def get_cache_menu():
    cache_key = 'menu_cache-1'
    cache_time = 5 * 60
    menus = cache.get(cache_key)
    if not menus:
        menus = Category.objects.filter(active=True)
        cache.set(cache_key, menus, cache_time)
    return menus


def get_site_config():
    cache_key = 'site_config_1'
    cache_time = 5 * 60
    menus = cache.get(cache_key)
    if not menus:
        menus = SiteSettings.objects.last()
        cache.set(cache_key, menus, cache_time)
    return menus


def get_latest_news(adet):
    cache_key = 'latest_new'+str(adet)+''
    cache_time = 5 * 60
    latest = cache.get(cache_key)
    if not latest:
        latest = News.objects.filter(active=True,category__active=True,sub_category__active=True).order_by("-id")[:adet].values('title','spot','slug','image','category__title','date');
        cache.set(cache_key, latest, cache_time)
    return latest


def get_trends_news(adet):
    cache_key = 'trend_news'+str(adet)+''
    cache_time = 5 * 60
    trends = cache.get(cache_key)
    if not trends:
        trends = News.objects.filter(active=True,category__active=True,sub_category__active=True).order_by("-viewed")[:adet].values('title','spot','slug','image','category__title','date','video_url','viewed');
        cache.set(cache_key, trends, cache_time)
    return trends


def get_videos_news(adet):
    cache_key = 'video_news_'+str(adet)+''
    cache_time = 5 * 60
    videos = cache.get(cache_key)
    if not videos:
        videos = News.objects.filter(category__active=True,sub_category__active=True,active=True).exclude(video_url="0").order_by("-id")[:adet].values('title','spot','slug','image','category__title','date','category__slug');
        cache.set(cache_key, videos, cache_time)
    return videos


def get_gallery_news(adet):
    cache_key = 'gallery_news_'+str(adet)+''
    cache_time = 5 * 60
    gallery = cache.get(cache_key)
    if not gallery:
        gallery = News.objects.filter(category__active=True,sub_category__active=True).filter(
            pk__in=NewsGallery.objects.filter(active=True).order_by("-id").values("parent")).order_by("-id")[:adet].values('title','spot','slug','image','category__title','date');
        cache.set(cache_key, gallery, cache_time)
    return gallery


def get_random_news(adet):
    cache_key = 'random_news_'+str(adet)+''
    cache_time = 5 * 60
    news = cache.get(cache_key)
    if not news:
        news = News.objects.filter(category__active=True,sub_category__active=True,active=True).order_by("?")[:adet].values('title','spot','slug','image','category__title','date','video_url');
        cache.set(cache_key, news, cache_time)
    return news


def show_menu():
    cache_key = 'cache_subcat'
    cache_time = 5 * 60
    cat = cache.get(cache_key)
    if not cat:
        cat = SubCategory.objects.filter(active=True,parent__active=True)
        cache.set(cache_key, cat, cache_time)
    context = {'menus': get_cache_menu(), 'sites': get_site_config(), 'subcat': cat,'reklam':reklamlar()}
    return context


register.inclusion_tag('site/header.html')(show_menu)


def show_left_menu():
    return {'leftmenu': get_cache_menu(), 'sites': get_site_config()}


register.inclusion_tag('site/leftmenu.html')(show_left_menu)


def show_rightbar(latest, trends, video,*args):
    return {'latest_news': get_latest_news(latest), 'trend_news': get_trends_news(trends),
            'video_news': get_videos_news(video),'reklam':args}


register.inclusion_tag('site/parts/right_sidebar.html')(show_rightbar)


def show_footer():
    return {'category': get_cache_menu(), 'sites': get_site_config()}


register.inclusion_tag('site/footer.html')(show_footer)


@register.filter
def in_category(subcat, category):
        return subcat.filter(parent=category,active=True).order_by("-id")[:5].values("image","title","slug")


## SİTE İNDEX SAYFASI

def index_rightbar(latest, gallery, video):
    return {'latest_news': get_latest_news(latest), 'gallery_news': get_gallery_news(gallery),
            'video_news': get_videos_news(video)}


register.inclusion_tag('site/parts/index/rightbar_index.html')(index_rightbar)


def index_left_trends(trends):
    return {'trend_news': get_trends_news(trends)}


register.inclusion_tag('site/parts/index/left_trends_index.html')(index_left_trends)


def index_section_morepost(adet):
    return {'news': get_random_news(adet)}


register.inclusion_tag('site/parts/index/section_more_post.html')(index_section_morepost)

@register.filter
def get_news(news, category):
    snews = [s for s in news if s.get("category__id") == category][:6]
    return snews


@register.filter
def get_news_video(news,adet):
    snews = [s for s in news if s.get("video_url") != "0"][:adet]
    return snews


@register.filter
def get_news_random(news):
    import random
    snews = [s for s in news]
    snews = random.sample(snews,10)
    return snews


@register.filter
def news_pagec(self):
    page_count = round(self / 2000)
    if self / 2000 > page_count:
        page_count += 1
    return page_count


@register.filter
def news_page(self,cur):
    page_count = round(self / 2000)
    if self / 2000 > page_count:
        page_count += 1
    if page_count == int(cur):
        return False
    return True

# Reklam
@register.filter
def reklam_getir(self, area):
    return self.filter(active=True,area=area)


def reklamlar():
    cache_key = 'reklamlar'
    cache_time = 20 * 5
    reklam = cache.get(cache_key)
    if not reklam:
        try:
            reklam = Reklam.objects.filter(active=True)
        except:
            reklam = None
        cache.set(cache_key, reklam, cache_time)
    return reklam