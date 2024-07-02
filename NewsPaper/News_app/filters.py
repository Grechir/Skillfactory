from django_filters import FilterSet, ChoiceFilter, DateFilter
from .models import Post
from django import forms

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем, должен чем-то напомнить Django дженерики.


# 2 разных метода


class PostFilter(FilterSet):
    content_type = ChoiceFilter(
        field_name='category_type',
        label='Publication type',
        empty_label='Все типы',
        choices=Post.choices
    )

    date_posted = DateFilter(
        field_name='date_post',
        label='Creation date after',
        lookup_expr='date__gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:

        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post

        # В fields мы описываем по каким полям модели будет производиться фильтрация
        fields = {
           # поиск по названию
           'title': ['icontains'],
           'post_category': ['exact'],
       }



