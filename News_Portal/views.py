from django.urls import reverse_lazy

from .filters import PostFilter
from datetime import datetime
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import PostForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


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
        return super().form_valid(form)


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
