from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL


# Create your models here.
class Goal(models.Model):
    """
    Goal objects
    """
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User)
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
        super(Goal, self).save(*args, **kwargs)


class Subgoal(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.CharField(max_length=150, null=True, blank=True)
    goal = models.ForeignKey(Goal)
    end_date = models.DateField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Subgoal, self).save(*args, **kwargs)
