# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
# from .models import PostCategory
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def product_created(instance, **kwargs):
#
#     # Получаем все категории, к которым относится пост
#     categories = instance.post_category.all()
#
#     # Собираем все email пользователей, которые подписаны на эти категории
#     emails = User.objects.filter(
#         subscriptions__category__in=categories
#     ).values_list('email', flat=True)
#
#     # Формируем тему письма
#     subject = f'Новый пост в категории(ях): {", ".join(category.name for category in categories)}'
#
#     text_content = (
#         f'Пост: {instance.title}\n'
#         f'Автор: {instance.author}\n\n'
#         f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Пост: {instance.title}<br>'
#         f'Автор: {instance.author}<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>'
#     )
#     # отправляем письмо каждому подписчику по email
#     for email in emails:
#         print(f"Sending email to: {email}")
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#         print(f"Email sent to: {email}")




