"""Endpoint URL Configuration."""

import os
import uuid

import scipy.io.wavfile
import speech.api.Vokaturi as Vokaturi
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.models import User
from pydub import AudioSegment
from rest_framework import routers, serializers, viewsets

from . import models

#
# Launch Vokaturi
#

Vokaturi.load("speech/lib/Vokaturi_mac.so")

print("\n-- Vokaturi loaded. --\n")


#
# What do serialise?
#


class RecordingSerializer(serializers.HyperlinkedModelSerializer):
    """Define API representation."""

    clip = serializers.FileField(required=True)

    def create(self, validated_data):
        """Change filename, hashtags, and emotions to necessary."""
        # Set defaults for when quality is not valid.
        neutral = 0
        happy = 0
        sad = 0
        anger = 0
        fear = 0

        #
        # Convert from MP3 to WAV for first upload.
        #

        filename = os.path.join(settings.MEDIA_ROOT,
                                validated_data.get("clip").name)
        filename = validated_data.get("clip").temporary_file_path()

        filename_out = os.path.join(settings.MEDIA_ROOT,
                                    str(uuid.uuid4()) + ".wav")
        sound = AudioSegment.from_mp3(filename)
        sound.export(filename_out, format="wav")

        #
        # Find sentiment.
        #

        (sample_rate, samples) = scipy.io.wavfile.read(filename_out)

        print("\nGETTING FILES DONE!\n\n")

        # Allocate Vokaturi sample array.

        buffer_length = len(samples)
        c_buffer = Vokaturi.SampleArrayC(buffer_length)

        if samples.ndim == 1:
            # Mono
            c_buffer[:] = samples[:] / 32768.0
        else:
            # Stereo. Should never happen.
            c_buffer[:] = 0.5 * (samples[:, 0] + samples[:, 1]) / 32768.0

        # Create voice and fill with samples.

        voice = Vokaturi.Voice(sample_rate, buffer_length)
        voice.fill(buffer_length, c_buffer)

        # Find sentiment, final step.

        quality = Vokaturi.Quality()
        emotionProbabilities = Vokaturi.EmotionProbabilities()
        voice.extract(quality, emotionProbabilities)

        if quality.valid:
            neutral = int(emotionProbabilities.neutrality)
            happy = int(emotionProbabilities.happiness)
            sad = int(emotionProbabilities.sadness)
            anger = int(emotionProbabilities.anger)
            fear = int(emotionProbabilities.fear)

        #
        # Get a transcript of what is said.
        #

        # Get transcript.

        # Delete WAV file.

        #
        # Analyse categories from NLP.
        #

        return models.Recording(neutral=neutral, happy=happy, sad=sad,
                                angry=anger, fear=fear, clip=null,
                                **validated_data)

    class Meta:
        """Meta models, what is shown."""

        model = models.Recording
        fields = ('clip', 'hashtags', 'happy',
                  'neutral', 'fear', 'sad', 'angry')


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
router.register(r'recordings', RecordingViewSet)
router.register(r'hashtag', HashtagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]


# Show media files if not in debug.

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
