"""Endpoint URL Configuration."""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from . import models

#
# What do serialise?
#


class RecordingSerializer(serializers.HyperlinkedModelSerializer):
    """Define API representation."""

    clip = serializers.FileField(required=True)

    class Meta:
        """Meta models, what is shown."""

        model = models.Recording
        fields = ('clip', 'hashtags', 'happy',
                  'neutral', 'fear', 'sad', 'angry')


class RecordingViewSet(viewsets.ModelViewSet):
    """Define view behaviour."""

    queryset = models.Recording.objects.all()
    serializer_class = RecordingSerializer

    def perform_create(self, serializer):
        """Change filename, hashtags, and emotions to necessary."""
        serializer.save(emotions={'test': 45})


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
router.register(r'recordings', RecordingViewSet)
router.register(r'hashtag', HashtagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]

# Show media files if not in debug.

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
