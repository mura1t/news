from django.contrib import admin
from .models import *


class NewsCommentAdmin(admin.ModelAdmin):
    class Meta:
        model = NewsComment
    readonly_fields = ["date"]
    list_display = ("parent","user","content",)


admin.site.register(NewsComment,NewsCommentAdmin)


class ProductCommentAdmin(admin.ModelAdmin):
    class Meta:
        model = NewsComment
    readonly_fields = ["date"]
    list_display = ("parent","user","content",)


admin.site.register(ProductsComment,ProductCommentAdmin)