import django_filters
from django import forms
from django.db import models
from django.forms import DateInput
from django_filters import FilterSet
from django_filters.widgets import RangeWidget

from .models import Post


class PostFilter(FilterSet):
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            "title": ["icontains"],
            # количество товаров должно быть больше или равно
            "author__user__username": ["icontains"],
            "creation_time": ["gt"],
        }
        filter_overrides = {
            models.DateTimeField: {
                "filter_class": django_filters.DateFilter,
                "extra": lambda f: {
                    "widget": DateInput(attrs={"type": "date"}),
                },
            }
        }
