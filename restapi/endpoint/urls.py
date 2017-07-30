"""Endpoint URL Configuration."""

from django.conf.urls import include, url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from . import models

#
# What do serialise?
#


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Define API representation."""

    class Meta:
        """Meta models, what is shown."""

        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    """Define view behaviour."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecordingSerializer(serializers.HyperlinkedModelSerializer):
    """Define API representation."""

    class Meta:
        """Meta models, what is shown."""

        model = models.Recording
        fields = ('clip', 'date', 'filename', 'hashtags', 'emotions')


class RecordingViewSet(viewsets.ModelViewSet):
    """Define view behaviour."""

    queryset = models.Recording.objects.all()
    serializer_class = RecordingSerializer


class HashtagSerializer(serializers.HyperlinkedModelSerializer):
    """Define API representation."""

    class Meta:
        """Meta models, what is shown."""

        model = models.Hashtag
        fields = ('tag', )


class HashtagViewSet(viewsets.ModelViewSet):
    """Define view behaviour."""

    queryset = models.Hashtag.objects.all()
    serializer_class = HashtagSerializer


# Determine routing conf.

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'recordings', RecordingViewSet)
router.register(r'hashtag', HashtagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
