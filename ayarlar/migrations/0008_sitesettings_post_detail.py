# Generated by Django 2.0 on 2018-09-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ayarlar', '0007_auto_20180908_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='post_detail',
            field=models.CharField(default=1, help_text='Haber detayında sayfa başına düşen karakter sayısı', max_length=10, verbose_name='Haber Detay Karakter'),
            preserve_default=False,
        ),
    ]