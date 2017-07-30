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
    transcript = models.CharField(null=True, blank=True, max_length=5000)

    # Emotions

    happy = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    sad = models.IntegerField(default=0)
    angry = models.IntegerField(default=0)
    fear = models.IntegerField(default=0)
