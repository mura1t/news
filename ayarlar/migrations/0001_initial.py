# Generated by Django 2.0 on 2018-09-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('desc', models.TextField()),
                ('logo', models.ImageField(upload_to='site')),
                ('logo_nav', models.ImageField(upload_to='site')),
                ('icon', models.ImageField(upload_to='site')),
                ('keywords', models.CharField(max_length=150)),
                ('facebook', models.CharField(default='0', max_length=100)),
                ('twitter', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('linkedin', models.CharField(max_length=100)),
                ('pinterest', models.CharField(max_length=100)),
                ('youtube', models.CharField(max_length=100)),
                ('google_plus', models.CharField(max_length=100)),
                ('tumlbr', models.CharField(max_length=100)),
            ],
        ),
    ]