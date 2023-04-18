# from django.views.generic import ListView, DetailView
#
# from .models import Post
#
# #
# #
# class NewsList(ListView):
#     # Указываем модель, объекты которой мы будем выводить
#     model = Post
#     # Поле, которое будет использоваться для сортировки объектов
#     ordering = "creation_time"
#     # Указываем имя шаблона, в котором будут все инструкции о том,
#     # как именно пользователю должны быть показаны наши объекты
#     template_name = "news.html"
#     # Это имя списка, в котором будут лежать все объекты.
#     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
#     context_object_name = "news"
#
#
# class NewsDetail(DetailView):
#     # Модель всё та же, но мы хотим получать информацию по отдельному товару
#     model = Post
#     # Используем другой шаблон — product.html
#     template_name = "post.html"
#     # Название объекта, в котором будет выбранный пользователем продукт
#     context_object_name = "post"


from django.views.generic import ListView, DetailView

from .filters import PostFilter
from .models import Post


from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = "-creation_time"
    template_name = "news.html"
    context_object_name = "news"
    paginate_by = 10

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context["time_now"] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context["next_sale"] = None
        return context

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context["filterset"] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
