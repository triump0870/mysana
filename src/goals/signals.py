from django.db.models.signals import post_save
from django.dispatch import receiver
from goals.models import Goal
from goals.tasks import send_creation_email, send_update_email

import logging

logger = logging.getLogger('project')


@receiver(post_save, sender=Goal)
def create_notification(sender, instance=None, created=False, **kwargs):
    try:
        if created:
            task_id = send_creation_email.delay(instance.id)
            logger.info("Signal worked for [%s]" % instance.id)
            logger.info("A task was created with id [%s]" % task_id)
        else:
            task_id = send_update_email.delay(instance.id)
            logger.info("Signal worked for [%s]" % instance.id)
            logger.info("A task was updated with id [%s]" % task_id)
    except:
        logger.info("signal didn't work")

# @receiver(post_save, sender=Goal)
# def update_notification(*kw):
#     pass
