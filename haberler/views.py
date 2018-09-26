from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from haberler.models import News, NewsGallery
from comments.models import NewsComment
from django.http import Http404
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ayarlar.models import SiteSettings
from .templatetags.menu import get_site_config
from next_prev import next_in_order, prev_in_order
from django.views.decorators.cache import cache_page
from haberler.templatetags.menu import reklamlar


# @cache_page(11)
def news_list(request, slug):
    page = request.GET.get('sayfa', 1)
    sayfa_adet = SiteSettings.objects.get().page_size
    try:
        news_total = News.objects.filter(active=True, category__slug=slug).count()
        news = News.objects.filter(active=True, category__slug=slug).order_by("-id")[:(int(page) + 2) * sayfa_adet].values('id','title','spot','slug','image','category__title','date');
        if not news:
            news = News.objects.filter(active=True, sub_category__slug=slug).order_by("-id")[:(int(page) + 1) * sayfa_adet].values('id','title','spot','slug','image','category__title','date');
            news_total = News.objects.filter(active=True, sub_category__slug=slug).count()
    except:
        news = None; news_total = 0
    count = 0
    if news:
        count = news_total
        if news_total / sayfa_adet > round(news_total / sayfa_adet):
            count = round(news_total / sayfa_adet) + 1
        paginator = Paginator(news, sayfa_adet)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
    else:
        # raise Http404()
        messages.add_message(request, messages.INFO, "Aradığınız sayfa  ya da haber bulunumadı")
    context = {
        'news': news,
        'count': count,
        'site': get_site_config(),
    }
    return render(request, "haberler/news_list.html", context)


# @cache_page(400)
def news_detail(request, slug):
    context = {}
    try:
        news = News.objects.filter(active=True, slug=slug)
        post_news = News.objects.get(active=True, slug=slug)
    except:
        post_news = None
        raise Http404()
    if news and post_news:
        cache_key = 'trend_news_detail'
        cache_time = 60 * 10
        trends = cache.get(cache_key)
        try:
            similar_news = News.objects.filter(active=True,sub_category=post_news.sub_category).exclude(slug=slug).order_by("-id")[:5].values("title","slug","image","category__title","category__slug","user__username","spot","date","user__profile__image","detail","video_url")
        except:
            similar_news = None
        if not trends:
            trends = News.objects.filter(active=True).order_by("-viewed")[:4].values("title","slug","date","image","category__title")
            cache.set(cache_key, trends, cache_time)
        paging_ch = int(SiteSettings.objects.all().get().post_detail)
        sayfa = int(request.GET.get("sayfa", 1))
        context = {
            'news': news,
            'char': paging_ch,
            'next_news': next_in_order(post_news),
            'prev_news': prev_in_order(post_news, loop=True),
            'similar_news': similar_news,
            'detailtext': post_news.detail[((sayfa - 1) * paging_ch):(((sayfa - 1) * paging_ch) + paging_ch)],
            'comments': NewsComment.objects.filter(parent__in=News.objects.filter(slug=slug), active=True),
            'trends': trends,
            'gallery': NewsGallery.objects.filter(parent=post_news, active=True),
            'site': get_site_config(),
            'reklam':reklamlar()
        }
    if request.method == "POST":
        try:
            if not request.user.is_authenticated:
                NewsComment.objects.create(user=request.POST.get("name"), parent=post_news, content=request.POST.get("content"),active=False, mail=request.POST.get("email"), web_site=request.POST.get("url"))
            else:
                NewsComment.objects.create(user=request.user.username,parent=post_news,
                                           content=request.POST.get("content"), active=False,
                                           mail=request.user.email, web_site=request.POST.get("url"))
            messages.add_message(request, messages.SUCCESS, "Yorum eklendi . Yönetici onayından sonra burada görebilirsiniz")
        except:
            pass

    else:
        if post_news:
            post_news.viewed += 1
            post_news.save()
    #yüklenen haberler
    numbers_list = News.objects.filter(active=True,sub_category=post_news.sub_category).exclude(id=post_news.id).order_by("-id")[:100]
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 1)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    context.update({'numbers':numbers})
    return render(request, "haberler/news_detail.html", context)


def get_latest_news(adet):
    cache_key = 'latest_new'
    cache_time = 60 * 10
    latest = cache.get(cache_key)
    if not latest:
        latest = News.objects.filter(active=True).order_by("-id")
        cache.set(cache_key, latest, cache_time)
    return latest


def last_news(request):
    template = "haberler/last_news.html"
    context = {'last_news': get_latest_news(2)}
    return render(request, template, context)


def addnews(request):
    # spot = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."
    # detail = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."
    # image = "resim4.jpg"
    # tags = "deneme ,tags ,lar"
    index = 0
    # news = News.objects.filter(active=True).order_by("-id")
    # for i in news:
    #     i.save()
    # adres = TamSiparisler.objects.last()
    # adres.product_text = "<h1>deneme</h1>"
    # adres.save()
    # while index <= 70000:
    #     News.objects.create(title="Boks şaşkın, yanlış kararlarla kendini göstermeye devam ediyor" + str(index) + "",
    #                         spot=spot, detail=detail, image=image, user_id=1, category_id=3, tags=tags,
    #                         sub_category_id=1)
    #     index += 1
    return render(request, "haberler/addnews.html")

# def error_404_view(request, exception):
#     data = {"name": "ThePythonDjango.com"}
#     return render(request,'site/error404.html', data)
