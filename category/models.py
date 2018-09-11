from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        unique_slug = slugify(self.title.replace('ı', 'i'))
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="subcategory")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.parent.slug + "-" + self.title.replace('ı', 'i'))
        return super(SubCategory, self).save(*args, **kwargs)
