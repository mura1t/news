from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from smart_selects.db_fields import ChainedForeignKey
import re
from ckeditor.fields import RichTextField
from django.utils.crypto import get_random_string


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Başlık")
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    spot = models.CharField(max_length=255)
    detail = RichTextField(verbose_name="İçerik")
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="News")
    user = models.ForeignKey(User, on_delete=None)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    sub_category = ChainedForeignKey("SubCategory", chained_field='category', chained_model_field='parent')
    video_url = models.CharField(max_length=200, default="0",
                                 help_text="Eğer video eklemek istemiyorsanız burası 0 olarak kalmalı")
    active = models.BooleanField(default=True)
    viewed = models.IntegerField(verbose_name="Görüntülenme Sayısı", default=0)
    tags = models.CharField(max_length=200,
                            help_text="Lütfen kelimelerin arasında virgül kullanınız ve boşluk kullanmayınız")

    def __str__(self):
        return self.title

    def tags_split(self):
        return self.tags.split(',')

    class Meta:
        ordering = ('title','pk')


@receiver(pre_save, sender=News)
def NewsSlug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            '%s-%s-%s' % (instance.sub_category.slug, instance.title, get_random_string(10, "1234567890")))
    else:
        instance.slug = slugify(
            '%s-%s-%s' % (instance.sub_category.slug, instance.title, str(instance.slug.split("-").pop())))


@receiver(pre_save, sender=News)
def NewsTags(sender, instance, *args, **kwargs):
    instance.tags = instance.tags.lower()
    instance.tags = instance.tags.replace("ı", "i").replace("ü", "u").replace("ç", "c").replace("ş", "s").replace("ğ",
                                                                                                                  "g").replace(
        "ö", "o")
    if instance.tags.startswith(',,') or instance.tags.endswith(',,'):
        instance.tags = instance.tags.replace(',,', "")
    if not (instance.tags.startswith(',') and instance.tags.endswith(',')):
        instance.tags = ('%s%s%s' % (",", instance.tags, ","))
    instance.tags = instance.tags.replace(",,", ",");
    instance.tags = re.sub('[^.,a-zA-Z ]', '', instance.tags)


class NewsGallery(models.Model):
    parent = models.ForeignKey("News", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="NewsGallery")
    active = models.BooleanField(default=True)


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

