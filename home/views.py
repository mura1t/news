from django.shortcuts import render, Http404,redirect,reverse,HttpResponseRedirect,HttpResponse
from haberler.models import News
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haberler.templatetags import menu
from django.views.decorators.cache import cache_page
from ayarlar.models import SiteSettings
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm,AuthenticationForm
from django.contrib.auth import update_session_auth_hash,login, authenticate, logout as log_out
from django.contrib import messages
from .forms import LoginForm
from htmlmin.decorators import minified_response


def test_page(request):
    return render(request, 'test.html',)


# @cache_page(60*2)
# @minified_response
def home_view(request):
    template = "site/index.html"
    news = News.objects.filter(active=True)[:120].values("id","title","slug","category__slug","image","category__id","category__title","date","video_url")
    context = {
        'category': menu.get_cache_menu(),
        'news': news,
        'videos_news': menu.get_videos_news(5),
        'site': menu.get_site_config(),
        'reklam': menu.reklamlar()
    }
    return render(request, template, context)


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.user.is_authenticated:
        return redirect(reverse("home_view"))
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if user:
            if request.GET.get("next"):
                return HttpResponseRedirect(request.GET.get("next"))
            else:
                return redirect(reverse("home_view"))
    else:
        messages.add_message(request, messages.INFO, form.errors)

    return render(request, "user/login.html", context)


def logout(request):
    log_out(request)
    return redirect(reverse("home_view"))


@login_required
def log_settings(request):
    user = request.user
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'user/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def log_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # if User.objects.filter(username=form.user.username).exists():
            #     user = User.objects.get(username=form.user.username)
            #     user.email =
            messages.success(request, 'Parolan kaydeildi')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'user/password.html', {'form': form})


def search_view(request):
    query = request.GET.get('q')
    query = query
    news_list = None
    news = None
    if query:
        news_list = News.objects.filter(active=True).values('title','spot','slug','image','category__title','date','detail');
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
    news = None ; count = 0
    try:
        user = User.objects.get(username=slug)
    except:
        user = None
        raise Http404
    if user:
        news = News.objects.filter(user=user,active=True)
        page = request.GET.get('sayfa', 1)
        page_size = SiteSettings.objects.get().page_size
        try:
            count =round(News.objects.filter(active=True,user=user).count() / page_size)
        except:
            count = 0
        paginator = Paginator(news, page_size)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
    context = {
        'user': user,
        'news': news,
        'count': count,
    }
    return render(request, template, context)


def tags_filter(request, slug):
    template = "site/tags.html"
    news_list = None
    news = None
    if slug:
        news_list = News.objects.filter(active=True, tags__icontains="," + slug + "" + ",").values('title','spot','slug','image','category__title','date');
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
