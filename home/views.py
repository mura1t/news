from django.shortcuts import render, HttpResponse
from haberler.models import News
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haberler.templatetags import menu
from django.shortcuts import render_to_response
from django.template import RequestContext


def home_view(request):
    template = "site/index.html"
    context = {
        'category': menu.get_cache_menu(),
        'news': News.objects.filter(active=True),
        'videos_news': menu.get_videos_news(5),
        'site': menu.get_site_config(),
    }
    return render(request, template, context)


def search_view(request):
    query = request.GET.get('q')
    query = query
    news_list = None
    news = None
    if query:
        news_list = News.objects.filter(active=True)
        news_list = news_list.filter(
            Q(title__icontains=query) |
            Q(spot__icontains=query) |
            Q(detail__icontains=query)

        ).distinct()

    if news_list:
        page = request.GET.get('sayfa', 1)
        paginator = Paginator(news_list, 2)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
    context = {
        'search_list': news,
    }
    return render(request, "site/search.html", context)


def takimimiz(request):
    return render(request, "site/author/team.html", {'user': User.objects.all()})


def author_detail(request, slug):
    template = "site/author/author_details.html"
    try:
        user = User.objects.get(username=slug)
    except:
        user = None
    if user:
        news = News.objects.filter(user=user)
    else:
        news = None
    if news:
        page = request.GET.get('sayfa', 1)
        paginator = Paginator(news, 2)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
    context = {
        'user': user,
        'news': news,
    }
    return render(request, template, context)


def tags_filter(request, slug):
    template = "site/tags.html"
    news_list = None
    news = None
    if slug:
        news_list = News.objects.filter(active=True, tags__icontains="," + slug + "" + ",")
    if news_list:
        page = request.GET.get('sayfa', 1)
        paginator = Paginator(news_list, 10)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

    context = {'news': news, 'slug': slug}
    return render(request, template, context)



def notfoundpage(request):
    return render(request, "site/error404.html")
