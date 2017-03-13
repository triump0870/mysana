import logging

from celery.decorators import task
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

    # template = loader.get_template("email/create_goal.html")
    subject = "Mysana Notification"

    # html_message = template.render({
    #     "user": goal.user,
    #     "goal": goal.title
    # })

    logger.info("sending email for [%s]" % goal.id)
    send_mail(
        subject,
        '',
        settings.EMAIL_FROM,
        ["rohan@rohanroy.com"],
        # html_message=html_message,
        fail_silently=False
    )
    logger.info("Email was sent to [%s]" % goal.user.email)


@task()
def daily_notification():
    subject = "Mysana Daily Notification"
    template = loader.get_template("email/daily_notification.html")

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
            # html_message=html_message,
            fail_silently=False
        )
        logger.info("Email was sent to [%s]" % user.email)
