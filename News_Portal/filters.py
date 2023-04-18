from django_filters import FilterSet
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
            "author": ["iexact"],
            "creation_time": ["gt"],
        }
