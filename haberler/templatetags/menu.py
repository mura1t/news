from django import template
from haberler.models import News, NewsGallery

register = template.Library()
from category.models import Category,SubCategory
from django.core.cache import cache
from ayarlar.models import SiteSettings


def get_cache_menu():
    cache_key = 'menu_cache-1'
    cache_time = 60 * 10
    menus = cache.get(cache_key)
    if  menus:
        menus = Category.objects.filter(active=True)
        cache.set(cache_key, menus, cache_time)
    return menus


def get_site_config():
    cache_key = 'site_config_1'
    cache_time = 60 * 10
    menus = cache.get(cache_key)
    if not  menus:
        menus = SiteSettings.objects.last()
        cache.set(cache_key, menus, cache_time)
    return menus


def get_latest_news(adet):
    cache_key = 'latest_new'+str(adet)+''
    cache_time = 60 * 10
    latest = cache.get(cache_key)
    if not latest:
        latest = News.objects.filter(active=True).order_by("-id")[:adet].values('title','spot','slug','image','category__title','date');
        cache.set(cache_key, latest, cache_time)
    return latest


def get_trends_news(adet):
    cache_key = 'trend_news'+str(adet)+''
    cache_time = 60 * 10
    trends = cache.get(cache_key)
    if not trends:
        trends = News.objects.filter(active=True).order_by("-viewed")[:adet].values('title','spot','slug','image','category__title','date');
        cache.set(cache_key, trends, cache_time)
    return trends


def get_videos_news(adet):
    cache_key = 'video_news_'+str(adet)+''
    cache_time = 60 * 10
    videos = cache.get(cache_key)
    if not videos:
        videos = News.objects.filter(active=True).exclude(video_url="0").order_by("-id")[:adet].values('title','spot','slug','image','category__title','date','category__slug');
        cache.set(cache_key, videos, cache_time)
    return videos


def get_gallery_news(adet):
    cache_key = 'gallery_news_'+str(adet)+''
    cache_time = 60 * 10
    gallery = cache.get(cache_key)
    if not gallery:
        gallery = News.objects.filter(active=True).filter(
            pk__in=NewsGallery.objects.filter(active=True).order_by("-id").values("parent")).order_by("-id")[:adet].values('title','spot','slug','image','category__title','date');
        cache.set(cache_key, gallery, cache_time)
    return gallery


def get_random_news(adet):
    cache_key = 'random_news_'+str(adet)+''
    cache_time = 60 * 10
    news = cache.get(cache_key)
    if not news:
        news = News.objects.filter(active=True).order_by("?")[:adet].values('title','spot','slug','image','category__title','date');
        cache.set(cache_key, news, cache_time)
    return news


def show_menu():  # burada newsleri sayılo getir
    context = {'menus': get_cache_menu(), 'sites': get_site_config(), 'subcat': SubCategory.objects.filter(active=True)}
    return context


register.inclusion_tag('site/header.html')(show_menu)


def show_left_menu():
    return {'leftmenu': get_cache_menu(), 'sites': get_site_config()}


register.inclusion_tag('site/leftmenu.html')(show_left_menu)


def show_rightbar(latest, trends, video):
    return {'latest_news': get_latest_news(latest), 'trend_news': get_trends_news(trends),
            'video_news': get_videos_news(video)}


register.inclusion_tag('site/parts/right_sidebar.html')(show_rightbar)


def show_footer():
    return {'category': get_cache_menu(), 'sites': get_site_config()}


register.inclusion_tag('site/footer.html')(show_footer)


@register.filter
def in_category(subcat, category):
    return subcat.filter(parent=category).order_by("-id")[:5].values("image","title","slug")


## SİTE İNDEX SAYFASI

def index_rightbar(latest, gallery, video):
    return {'latest_news': get_latest_news(latest), 'gallery_news': get_gallery_news(gallery),
            'video_news': get_videos_news(video)}


register.inclusion_tag('site/parts/index/rightbar_index.html')(index_rightbar)


def index_left_trends(trends):
    return {'trend_news': get_trends_news(trends)}


register.inclusion_tag('site/parts/index/left_trends_index.html')(index_left_trends)


def index_section_zero(adet):
    return {'randoms': get_random_news(adet)}


register.inclusion_tag('site/parts/index/section_zero.html')(index_section_zero)


def index_section_one(cat, adet):
    cache_key = 'news_category_' + str(cat) + ''
    cache_time = 60 * 10
    news = cache.get(cache_key)
    if not news:
        news = News.objects.filter(category__id=cat).order_by("-id")[:adet].values('title','spot','slug','image','category__title','date','category__slug');
        cache.set(cache_key, news, cache_time)

    return {'news': news}


register.inclusion_tag('site/parts/index/section_one.html')(index_section_one)


def index_section_two_video():
    return {'news': get_videos_news(5)}


register.inclusion_tag('site/parts/index/section_two_video.html')(index_section_two_video)


def index_section_tree(cat,adet):
    cache_key = 'news_category_' + str(cat) + ''
    cache_time = 60 * 10
    news = cache.get(cache_key)
    if not news:
        news = News.objects.filter(category__id=cat).order_by("-id")[:adet].values('id','title','spot','slug','image','category__title','date','category__slug');
        cache.set(cache_key, news, cache_time)
    return {'news': news}


register.inclusion_tag('site/parts/index/section_tree.html')(index_section_tree)


def index_section_four(cat,adet):
    cache_key = 'news_category_' + str(cat) + ''
    cache_time = 60 * 10
    news = cache.get(cache_key)
    if not news:
        news = News.objects.filter(category__id=cat,active=True).order_by("-id")[:adet].values('id','title','spot','slug','image','category__title','date','category__slug');
        cache.set(cache_key, news, cache_time)
    return {'news': news}


register.inclusion_tag('site/parts/index/section_four.html')(index_section_four)


def index_section_morepost(adet):
    return {'news': get_random_news(adet)}


register.inclusion_tag('site/parts/index/section_more_post.html')(index_section_morepost)
