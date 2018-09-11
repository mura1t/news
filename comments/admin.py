from django.contrib import admin
from .models import *


class NewsCommentAdmin(admin.ModelAdmin):
    class Meta:
        model = NewsComment
    readonly_fields = ["date"]


admin.site.register(NewsComment,NewsCommentAdmin)