import logging
import os
from datetime import datetime

from celery.decorators import task
from celery.schedules import crontab
from celery.task import periodic_task
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
        "user": goal.user.name.title(),
        "goal": goal.title,
        "url": "http://" + os.environ.get('SERVER_NAME', 'mysana.rohanroy.com') + goal.get_absolute_url()
    })

    logger.info("sending email for [%s]" % goal.id)
    try:
        send_mail(
            subject,
            '',
            settings.EMAIL_FROM,
            [goal.user.email],
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
        "user": goal.user.name.title(),
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
            [goal.user.email],
            html_message=html_message,
            fail_silently=False
        )
        logger.info("Email was sent to [%s]" % goal.user.email)
    except:
        logger.info("Email was not sent to [%s]" % goal.user.email)


@periodic_task(run_every=crontab(hour="9", minute="0"))
def daily_notification():
    subject = "Mysana Daily Notification"
    template = loader.get_template("goals/email/daily_notification.html")

    users = User.objects.all()
    for user in users:
        goals = user.goal_set.filter(completed=False)
        logger.info("Goals count for user %s is %s" % (user.id, goals.count()))
        if goals.count() > 1:
            html_message = template.render({
                "user": user.name.title(),
                "goals": goals,
                "server": os.environ.get('SERVER_NAME', 'mysana.rohanroy.com')
            })
            logger.info("sending daily notifications for user [%s]" % user.id)
            send_mail(
                subject,
                '',
                settings.EMAIL_FROM,
                [user.email],
                html_message=html_message,
                fail_silently=False
            )
            logger.info("Daily notifications was sent to [%s]" % user.email)


@periodic_task(run_every=crontab(hour="10", minute="0"))
def overdue_task():
    template = loader.get_template("goals/email/overdue_notification.html")
    now = datetime.now()

    users = User.objects.all()
    for user in users:
        goals = user.goal_set.all().filter(end_date__gte=now, completed=False)
        logger.info("Goals count for user %s is %s" % (user.id, goals.count()))
        if goals.count() > 0:
            html_message = template.render({
                "user": user.name.title(),
                "goals": goals,
                "server": os.environ.get('SERVER_NAME', 'mysana.rohanroy.com'),
                "count": goals.count()
            })
            subject = "You have %s overdue life goals in Mysana" % goals.count()

            logger.info("sending daily overdue notifications for user [%s]" % user.id)
            send_mail(
                subject,
                '',
                settings.EMAIL_FROM,
                [user.email],
                html_message=html_message,
                fail_silently=False
            )
            logger.info("Daily overdue notifications was sent to [%s]" % user.email)
