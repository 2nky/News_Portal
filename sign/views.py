from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import BaseRegisterForm

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = "/"


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name="premium")
    if not request.user.groups.filter(name="premium").exists():
        premium_group.user_set.add(user)
    return redirect("/")


def render_to_template(param, param1):
    pass


@login_required
def user_profile(request):
    return render(request, "sign/profile.html")


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name="common")
        common_group.user_set.add(user)
        return user


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name="authors")
    if not request.user.groups.filter(name="authors").exists():
        author_group.user_set.add(user)
    return redirect("/profile")
