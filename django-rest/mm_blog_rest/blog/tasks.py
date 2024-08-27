from datetime import datetime
from django.db.models import Count

from django.utils import timezone

from celery import shared_task
from models import BlogPost


@shared_task
def delete_one_year_old_posts_without_comments():
    posts_for_delete = BlogPost.objects.annotate(number_of_comments=Count('comment')) \
        .filter(created_at=datetime(year=timezone.now().year - 1, month=timezone.now().month, day=timezone.now().day),
                number_of_comments=0)

    ids_from_posts = [x.pk for x in posts_for_delete]
    posts_for_delete.delete()

    print(f"Successfully deleted posts with ids: {ids_from_posts}")