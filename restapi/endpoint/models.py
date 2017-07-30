"""Persistence classes for the REST endpoint."""
from django.db import models
from jsonfield import JSONField


class Hashtag(models.Model):
    """Model for categorical hashtags."""

    tag = models.CharField(max_length=63)


class Recording(models.Model):
    """Model for recorded files."""

    clip = models.FileField(null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    emotions = JSONField(default="{}")
