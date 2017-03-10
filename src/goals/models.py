from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from datetime import datetime
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


# Create your models here.
class Goal(models.Model):
    """
    Goal objects
    """
    title = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
    end_date = models.DateField()
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


class Subgoal(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=150, null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        if not self.end_date:
            self.end_date = self.goal.end_date
        else:
            self.validate_end_date()
        super(Subgoal, self).save(*args, **kwargs)

    def validate_end_date(self):
        if self.end_date < datetime.now().date():
            raise ValidationError("End date should not be in past")
