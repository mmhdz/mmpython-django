# Generated by Django 5.1 on 2024-08-16 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post_app', '0005_remove_blogpost_negative_rating_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpostvoting',
            old_name='blog',
            new_name='blog_post',
        ),
    ]