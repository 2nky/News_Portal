import logging
from datetime import timedelta, datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail
from News_Portal.models import PostCategory, Subscribers, Post, Category

OUR_SITE_URL = "http://127.0.0.1:8000"

logger = logging.getLogger(__name__)


def send_weekly_updates():
    categories = Category.objects.all()
    now = datetime.now()
    week_before = timedelta(weeks=1)

    for category in categories:
        posts = Post.objects.filter(category=category, creation_time__gte=now - week_before)
        subscribers = Subscribers.objects.filter(category=category)
        for person in subscribers:
            send_mail(
                subject="Новые статьи за неделю в любимом разделе",
                message="",
                html_message=render_to_string(
                    "weekly_news.html",
                    context={
                        "user": person.user,
                        "posts": posts,
                        "site_url": OUR_SITE_URL,
                    },
                    request=None,
                    using=None,
                ),
                from_email="pol9.f@yandex.ru",
                recipient_list=[person.user.email],
            )


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_updates,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="send_weekly_updates",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_updates'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
