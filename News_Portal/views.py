from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse

from django.views import View

from .filters import PostFilter
from datetime import datetime
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import PostForm, CategorySelectForm
from .models import Post, Subscribers
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .tasks import send_news_notification


class NewsList(ListView, LoginRequiredMixin):
    model = Post
    ordering = "-creation_time"
    template_name = "news.html"
    context_object_name = "news"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_now"] = datetime.utcnow()
        context["next_sale"] = None
        context["filterset"] = self.filterset
        context["is_not_author"] = not self.request.user.groups.filter(
            name="author"
        ).exists()
        context["form"] = CategorySelectForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        qs = self.filterset.qs

        category_form = CategorySelectForm(self.request.GET)
        if category_form.is_valid():
            qs = qs.filter(category=category_form.cleaned_data["category"])

        return qs


class NewsDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"


class Search(ListView):
    model = Post
    ordering = "-creation_time"
    template_name = "search.html"
    context_object_name = "news"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_now"] = datetime.utcnow()
        context["next_sale"] = None
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class NWCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = "News_Portal.add_post"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        response = super().form_valid(form)

        send_news_notification.delay(post.pk)

        return response


class NWUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = "News_Portal.change_post"


class NWDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("news_list")
    permission_required = "News_Portal.delete_post"


class ATCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = "News_Portal.add_post"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AT"
        return super().form_valid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AT"
        response = super().form_valid(form)

        for category in post.category.all():
            subscribers = Subscribers.objects.filter(category=category)
            message = render_to_string(
                "news_notification.html",
                context=None,
                request=None,
                using=None,
            )

            for person in subscribers:
                send_mail(
                    subject="Новая статья в твоем любимом разделе",
                    message="",
                    html_message=render_to_string(
                        "news_notification.html",
                        context={"user": person.user},
                        request=None,
                        using=None,
                    ),
                    from_email="pol9.f@yandex.ru",
                    recipient_list=[person.user.email],
                )
        return response


class ATUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = "News_Portal.change_post"


class ATDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("news_list")
    permission_required = "News_Portal.delete_post"


def save():
    pass


class AddSubscriber(View):
    def get(self, request, **kwargs):
        return render(request, "mailing.html", {"form": CategorySelectForm})

    def post(self, request, *args, **kwargs):
        form = CategorySelectForm(request.POST)
        form.is_valid()
        # chosen_category = Category.objects.get(pk=form.cleaned_data["category"])

        mailing, created = Subscribers.objects.get_or_create(
            user=request.user,
            category=form.cleaned_data["category"],
        )

        group = Group.objects.get(name="subscribers")
        request.user.groups.add(group)

        send_mail(
            subject="Вы успешно подписались на рассылку!",
            message=f'Спасибо, вы подписались на раздел {form.cleaned_data["category"]}',
            from_email="pol9.f@yandex.ru",
            recipient_list=[request.user.email],
        )
        return redirect("/profile")
