"""Persistence classes for the REST endpoint."""
from django.db import models


class Hashtag(models.Model):
    """Model for categorical hashtags."""

    tag = models.CharField(max_length=63)


class Recording(models.Model):
    """Model for recorded files."""

    date = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=255)
    hashtags = models.ManyToManyField(Hashtag)


class Emotion(models.Model):
    """Model for emotions and values."""

    emotion = models.CharField(max_length=63)
    value = models.IntegerField()
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
