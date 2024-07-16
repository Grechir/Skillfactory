from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, PostUpdate,
                    PostDelete, PostCreate, PostSearch, subscriptions)


urlpatterns = [
   # Path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<pk>', PostDetail.as_view(), name='post_detail'),

   # создание
   path('create/', PostCreate.as_view(), name='post_create'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),

   # редактирование
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),

   # удаление
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
