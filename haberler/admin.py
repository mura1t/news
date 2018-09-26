from django.contrib import admin
from .models import *


class NewsInline(admin.TabularInline):
    model = NewsGallery
    extra = 2
    tag_fields = ["tags"]


class NewsAdmin(admin.ModelAdmin):
    class Meta:
        model = News

    readonly_fields = ["slug", "date", "viewed", "user"]
    inlines = [NewsInline]
    search_fields = ['title', 'slug']
    list_filter = ("category", "date","active")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class SubCatInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class AdminCategory(admin.ModelAdmin):
    class Meta:
        model = Category

    inlines = [SubCatInline]
    list_display = ("id", "title")
    list_display_links = ("id", "title")


class SubCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = SubCategory

    list_display = ("id", "title")
    list_display_links = ("id", "title")

admin.site.register(Category, AdminCategory)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(News, NewsAdmin)
