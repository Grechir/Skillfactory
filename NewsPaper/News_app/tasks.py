from celery import shared_task

import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


from .models import Post, Category


@shared_task
def send_new_post_task(pk):

    # определение нового поста по Primary Key (pk)
    post = Post.objects.get(pk=pk)

    # Получаем все категории, к которым относится пост
    categories = post.post_category.all()

    # Собираем все email пользователей, которые подписаны на эти категории
    emails = User.objects.filter(subscriptions__category__in=categories).values_list('email', flat=True)

    # Формируем тему письма
    subject = f'Новый пост в категории(ях): {", ".join(category.name for category in categories)}'

    text_content = (
        f'Пост: {post.title}\n'
        f'Автор: {post.author}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'Пост: {post.title}<br>'
        f'Автор: {post.author}<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    # отправляем письмо каждому подписчику по email
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_weekly_posts_task():

    today = timezone.now()  # определяем текущее время
    last_week = today - datetime.timedelta(days=7)  # определяем время ровно на неделю назад от текущего времени
    posts = Post.objects.filter(created__gte=last_week)  # все посты, созданные за неделю
    categories = set(posts.values_list('post_category__name', flat=True))  # определение категорий постов за неделю

    # подписчики постов
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscriptions__user__email', flat=True))

    # формируем письмо
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': f'http://127.0.0.1:8000/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
