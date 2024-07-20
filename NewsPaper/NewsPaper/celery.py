import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'print_every_mon_8am': {
        'task': 'News_app.tasks.send_weekly_posts_task',
        'schedule': crontab('0', '8', 'Monday'),
    },
}
