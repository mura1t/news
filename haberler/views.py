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

def news_list(request, slug):
    page = request.GET.get('sayfa', 1)
    sayfa_adet = 15
    template = "haberler/news_list.html"
    try:
        news = News.objects.filter(active=True, category__slug=slug).order_by("-id")[:(int(page) +2) * sayfa_adet];
        if not news:
            news = News.objects.filter(active=True, sub_category__slug=slug).order_by("-id")[:(int(page) + 1) * sayfa_adet];
    except:
        news = None
    count =0
    if news:
        news_total = News.objects.filter(active=True,category__slug=slug).count()
        if news_total / sayfa_adet > round(news_total / sayfa_adet):
            count = round(news_total / sayfa_adet) + 1
        else:
            count = round(news_total / sayfa_adet)
        paginator = Paginator(news, sayfa_adet)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
    else:
        raise Http404()
        messages.add_message(request, messages.INFO, "Aradığınız sayfa  ya da haber bulunumadı")
    context = {
        'news': news,
        'count' :count,
        'site': get_site_config(),
    }
    return render(request, template, context)


def news_detail(request, slug):
    template = "haberler/news_detail.html";
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
            similar_news = News.objects.filter(sub_category=post_news.sub_category).exclude(slug=slug).order_by("-id")[:5]
        except:
            similar_news = None
        if not trends:
            trends = News.objects.filter(active=True).order_by("-viewed")[:4]
            cache.set(cache_key, trends, cache_time)
        paging_ch = int(SiteSettings.objects.all().get().post_detail)
        sayfa = int(request.GET.get("sayfa", 1))
        baslangic = ((sayfa - 1) * paging_ch)
        next = next_in_order(post_news)
        prev = prev_in_order(post_news, loop=True)
        context = {
            'news': news,
            'char': paging_ch,
            'next_news': next,
            'prev_news':prev,
            'similar_news': similar_news,
            'detailtext': post_news.detail[((sayfa - 1) * paging_ch):(baslangic + paging_ch)],
            'comments': NewsComment.objects.filter(parent__in=News.objects.filter(slug=slug), active=True),
            'trends': trends,
            'gallery': NewsGallery.objects.filter(parent=post_news, active=True),
            'site':get_site_config(),
        }
    if request.method == "POST":
        NewsComment.objects.create(user=request.POST.get("name"), parent=post_news, content=request.POST.get("content"),
                                   active=False, mail=request.POST.get("email"), web_site=request.POST.get("url"))
        messages.add_message(request, messages.SUCCESS,
                             "Yorum eklendi . Yönetici onayından sonra burada görebilirsiniz")
    else:
        if post_news:
            post_news.viewed += 1
            post_news.save()
    return render(request, template, context)


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
    news =  News.objects.filter(active=True).order_by("-id")
    for i in news:
        i.save()
    # while index <= 70000:
    #     News.objects.create(title="Boks şaşkın, yanlış kararlarla kendini göstermeye devam ediyor" + str(index) + "",
    #                         spot=spot, detail=detail, image=image, user_id=1, category_id=3, tags=tags,
    #                         sub_category_id=1)
    #     index += 1
    # return render(request, "haberler/addnews.html")

# def error_404_view(request, exception):
#     data = {"name": "ThePythonDjango.com"}
#     return render(request,'site/error404.html', data)
