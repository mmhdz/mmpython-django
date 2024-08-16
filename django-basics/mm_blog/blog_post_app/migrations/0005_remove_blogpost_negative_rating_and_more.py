# Generated by Django 5.1 on 2024-08-16 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post_app', '0004_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='negative_rating',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='positive_rating',
        ),
        migrations.CreateModel(
            name='BlogPostVoting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive_rating', models.IntegerField(default=0)),
                ('negative_rating', models.IntegerField(default=0)),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog_post_app.blogpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]