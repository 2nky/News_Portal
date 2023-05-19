from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from News_Portal.models import Subscribers, Post
from News_Portal.constants import OUR_SITE_URL


@shared_task
def send_news_notification(post_pk):
    post = Post.objects.get(pk=post_pk)

    for category in post.category.all():
        subscribers = Subscribers.objects.filter(category=category)

        for person in subscribers:
            send_mail(
                subject="Новая статья в твоем любимом разделе",
                message="",
                html_message=render_to_string(
                    "news_notification.html",
                    context={
                        "user": person.user,
                        "post": post,
                        "site_url": OUR_SITE_URL,
                    },
                    request=None,
                    using=None,
                ),
                from_email="pol9.f@yandex.ru",
                recipient_list=[person.user.email],
            )
