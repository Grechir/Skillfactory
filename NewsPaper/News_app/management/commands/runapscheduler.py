# import logging
# import signal
# import datetime
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.core.management.base import BaseCommand
# from django.template.loader import render_to_string
# from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from django.utils import timezone
#
# from News_app.models import Post, Category
#
# logger = logging.getLogger(__name__)
#
#
# def my_job():
#     today = timezone.now()
#     last_week = today - datetime.timedelta(days=7)
#     posts = Post.objects.filter(created__gte=last_week)
#     categories = set(posts.values_list('post_category__name', flat=True))
#     subscribers = set(Category.objects.filter(name__in=categories).values_list('subscriptions__user__email', flat=True))
#     html_content = render_to_string(
#         'weekly_post.html',
#         {
#             'link': f'http://127.0.0.1:8000/',
#             'posts': posts,
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject='Статьи за неделю',
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(day_of_week="fri", hour=18, minute=0, second=0),
#             id="my_job",  # The `id` assigned to each job MUST be unique
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added weekly job: 'delete_old_job_executions'.")
#
#         def shutdown_scheduler(signum, frame):
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
#
#         signal.signal(signal.SIGINT, shutdown_scheduler)
#         signal.signal(signal.SIGTERM, shutdown_scheduler)
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             shutdown_scheduler(None, None)

