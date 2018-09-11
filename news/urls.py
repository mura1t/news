from django.contrib import admin
from django.urls import path
from home.views import home_view,search_view,takimimiz,author_detail,tags_filter,notfoundpage
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home_view"),
    path('haberler/',include("haberler.urls")),
    path('arama/',search_view,name="search_view"),
    path('takimimiz',takimimiz,name="takimimiz"),
    path('yazarlar/<slug:slug>',author_detail,name="author_detail"),
    path('tags/<slug:slug>',tags_filter,name="tags"),
    path('sayfa-bulunamadi',notfoundpage,name="notfoundpage"),
    path('chaining/', include('smart_selects.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
