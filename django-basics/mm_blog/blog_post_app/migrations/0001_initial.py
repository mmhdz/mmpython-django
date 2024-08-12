# Generated by Django 5.1 on 2024-08-09 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=100)),
                ('registration_date', models.DateTimeField(verbose_name='the date user is registered')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_post_app.blogpost')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_post_app.blogpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_post_app.user')),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_post_app.user'),
        ),
    ]