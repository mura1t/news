from django.contrib import admin
from .models import *


class NewsInline(admin.TabularInline):
    model = NewsGallery
    extra = 2
    tag_fields = ["tags"]


class NewsAdmin(admin.ModelAdmin):
    class Meta:
        model = News

    readonly_fields = ["slug", "date", "viewed","user"]
    inlines = [NewsInline]
    search_fields = ['title','slug']
    list_filter = ("category","date")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class NewsGalleryAdmin(admin.ModelAdmin):
    class Meta:
        model = NewsGallery


admin.site.register(News, NewsAdmin)
admin.site.register(NewsGallery, NewsGalleryAdmin)
