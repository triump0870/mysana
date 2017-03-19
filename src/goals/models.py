from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

User = settings.AUTH_USER_MODEL


# Create your models here.
class Goal(models.Model):
    """
    Goal objects
    """
    title = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    description = models.TextField(help_text=_('optional'), null=True, blank=True)
    user = models.ForeignKey(User)
    end_date = models.DateField(help_text=_('format yyyy-mm-dd'))
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        ordering = ['end_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        self.validate_end_date()
        super(Goal, self).save(*args, **kwargs)

    def validate_end_date(self):
        if self.end_date < datetime.now().date():
            raise ValidationError("End date should not be in past")

    def is_completed(self):
        if self.completed:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse("apis:goal-details", kwargs={'pk': self.pk})
