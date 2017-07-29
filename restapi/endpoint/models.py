"""Persistence classes for the REST endpoint."""
from django.db import models


class Hashtag(models.Model):
    """Model for categorical hashtags."""

    tag = models.CharField(max_length=63)


class HashtagList(models.Model):
    """Intermediary model for categorical hashtags."""


class Recording(models.Model):
    """Model for recorded files."""

    filename = models.CharField(max_length=255)
