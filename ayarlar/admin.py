from django.contrib import admin
from .models import *


class SiteAdmin(admin.ModelAdmin):
    class Meta:
        model = SiteSettings

    def has_add_permission(self, request):
        count = SiteSettings.objects.all().count()
        if count < 1:
            return True
        else:
            return False

    fieldsets = [
        ('Genel Bilgiler', {
            'fields': ['title', 'desc', 'logo', 'logo_nav', 'icon', 'keywords', 'footer_text', 'top_banner',
                       'post_detail','domain','page_size']}),
        ('Sosyal Medya', {'fields': ['instagram', 'facebook', 'twitter', 'pinterest', 'google_plus', 'tumblr']}),
        ('İyzico Ödeme Ayarları',{'fields':['iyzi_api','iyzi_secret_key']})
    ]

admin.site.register(Profile)
admin.site.register(SiteSettings, SiteAdmin)
