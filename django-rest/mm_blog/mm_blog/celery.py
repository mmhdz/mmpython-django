import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm_blog.settings')


app = Celery('mm_blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-old-posts-with-no-comments': {
        'task': 'blog.tasks.delete_one_year_old_posts_without_comments',
        'schedule': crontab("0", "0"),
        'options': {
                    'expires': 60 * 60,
                },
    },
}