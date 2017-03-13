from django.db.models.signals import post_save
from django.dispatch import receiver
from goals.models import Goal
from goals.tasks import send_creation_email

import logging

logger = logging.getLogger('project')


@receiver(post_save, sender=Goal)
def create_notification(sender, instance=None, created=False, **kwargs):
    if created:
        send_creation_email.apply_async((instance.id,))
        logger.info("Signal worked for [%s]" % instance.id)
    logger.info("signal didn't work")

# @receiver(post_save, sender=Goal)
# def update_notification(*kw):
#     pass
