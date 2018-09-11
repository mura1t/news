from django.contrib import admin
from .models import Category, SubCategory


class SubCatInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class AdminCategory(admin.ModelAdmin):
    class Meta:
        model = Category

    inlines = [SubCatInline]


admin.site.register(Category, AdminCategory)
