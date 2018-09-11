# Generated by Django 2.0 on 2018-09-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ayarlar', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='google_plus',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='pinterest',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook',
            field=models.CharField(max_length=100),
        ),
    ]
