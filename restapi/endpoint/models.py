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

    happy = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    neutral = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    sad = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    angry = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    fear = models.DecimalField(default=0, decimal_places=4, max_digits=10)
