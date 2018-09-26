from django.contrib import admin
from django.urls import path
from home.views import home_view, search_view, takimimiz, author_detail, tags_filter, notfoundpage, login_view, logout,log_password,log_settings,test_page
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home_view"),
    path('test',test_page , name="test_page"),
    path('haberler/', include("haberler.urls")),
    path('arama/', search_view, name="search_view"),
    path('takimimiz', takimimiz, name="takimimiz"),
    path('yazarlar/<slug:slug>', author_detail, name="author_detail"),
    path('tags/<slug:slug>', tags_filter, name="tags"),
    path('sayfa-bulunamadi', notfoundpage, name="notfoundpage"),
    path('chaining/', include('smart_selects.urls')),
    # giris & cikis
    path('giris', login_view, name='login'),
    path('cikis', logout, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('settings/', log_settings, name='settings'),
    path('settings/password/', log_password, name='password'),
    # mağaza
    path('magaza/', include("shop.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
