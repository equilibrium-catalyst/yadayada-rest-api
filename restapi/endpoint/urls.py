"""Endpoint URL Configuration."""

from django.conf.urls import include, url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

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


# Determine routing conf.

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
