"""Persistence classes for the REST endpoint."""
from django.db import models
from jsonfield import JSONField


class Hashtag(models.Model):
    """Model for categorical hashtags."""

    tag = models.CharField(max_length=63)


class Recording(models.Model):
    """Model for recorded files."""

    date = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=255)
    hashtags = models.ManyToManyField(Hashtag)
    emotions = JSONField(default="{}")
