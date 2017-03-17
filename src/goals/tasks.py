import logging
import os

from celery.decorators import task
from celery.schedules import crontab
from celery.task.base import periodic_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template import loader

from goals.models import Goal

logger = logging.getLogger("project")
User = get_user_model()


@task()
def send_creation_email(id):
    goal = Goal.objects.get(id=id)

    template = loader.get_template("goals/email/create_goal.html")
    subject = "Mysana Notification"

    html_message = template.render({
        "user": goal.user.name,
        "goal": goal.title,
        "url": "http://" + os.environ.get('SERVER_NAME', 'mysana.rohanroy.com') + goal.get_absolute_url()
    })

    logger.info("sending email for [%s]" % goal.id)
    try:
        send_mail(
            subject,
            '',
            settings.EMAIL_FROM,
            ["rohan@rohanroy.com"],
            html_message=html_message,
            fail_silently=False
        )
        logger.info("Email was sent to [%s]" % goal.user.email)
    except:
        logger.info("Email was not sent to [%s]" % goal.user.email)


@task()
def send_update_email(id):
    goal = Goal.objects.get(id=id)
    if goal.is_completed():
        subject = "Mysana Task Completed Notification"
        status = "completed"
    else:
        subject = "Mysana Task Updation Notification"
        status = "updated"

    template = loader.get_template("goals/email/update_goal.html")

    html_message = template.render({
        "user": goal.user.name,
        "goal": goal.title,
        "status": status,
        "url": "http://" + os.environ.get('SERVER_NAME', 'mysana.rohanroy.com') + goal.get_absolute_url()
    })

    logger.info("sending email for [%s]" % goal.id)
    try:
        send_mail(
            subject,
            '',
            settings.EMAIL_FROM,
            ["rohan@rohanroy.com"],
            html_message=html_message,
            fail_silently=False
        )
        logger.info("Email was sent to [%s]" % goal.user.email)
    except:
        logger.info("Email was not sent to [%s]" % goal.user.email)


@periodic_task(run_every=(crontab(minute='2')))
def daily_notification():
    subject = "Mysana Daily Notification"
    template = loader.get_template("goals/email/daily_notification.html")

    users = User.objects.all()
    for user in users:
        goals = user.goal_set.all()

        html_message = template.render({
            "user": user,
            "goal": goals
        })
        logger.info("sending email for user [%s]" % user.id)
        send_mail(
            subject,
            '',
            settings.EMAIL_FROM,
            ["rohan@rohanroy.com"],
            html_message=html_message,
            fail_silently=False
        )
        logger.info("Email was sent to [%s]" % user.email)
