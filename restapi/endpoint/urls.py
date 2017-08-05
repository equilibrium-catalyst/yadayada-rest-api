"""Endpoint URL Configuration."""

import os
import uuid

import scipy.io.wavfile
import speech.api.Vokaturi as Vokaturi
import speech_recognition as sr
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.models import User
from pydub import AudioSegment
from rest_framework import routers, serializers, viewsets

from . import models, views

#
# Launch Vokaturi
#

Vokaturi.load("speech/lib/Vokaturi_mac.so")

#
# What do serialise?
#


class RecordingSerializer(serializers.HyperlinkedModelSerializer):
    """Define API representation."""

    clip = serializers.FileField(required=True)

    def create(self, validated_data):
        """Change non-given attributes to necessary values."""
        # Set defaults for when quality is not valid.
        neutral = 0
        happy = 0
        sad = 0
        anger = 0
        fear = 0
        transcript = ""

        clip = validated_data.pop("clip")
        filename = clip.temporary_file_path()

        # Verify proper audio file.

        recording = models.Recording(neutral=neutral, happy=happy, sad=sad,
                                     angry=anger, fear=fear, clip=clip,
                                     transcript="")
        recording.save()

        #
        # Convert from MP3 to WAV for first upload.
        #

        filename_out = os.path.join(settings.MEDIA_ROOT,
                                    str(uuid.uuid4()) + ".wav")
        sound = AudioSegment.from_mp3(filename)
        sound.export(filename_out, format="wav")

        #
        # Find sentiment.
        #

        (sample_rate, samples) = scipy.io.wavfile.read(filename_out)

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
            recording.neutral = round(100 * emotionProbabilities.neutrality)
            recording.happy = round(100 * emotionProbabilities.happiness)
            recording.sad = round(100 * emotionProbabilities.sadness)
            recording.anger = round(100 * emotionProbabilities.anger)
            recording.fear = round(100 * emotionProbabilities.fear)

            recording.save()

        #
        # Get a transcript of what is said.
        #

        # Get transcript.

        r = sr.Recognizer()
        with sr.AudioFile(filename_out) as source:
            audio = r.record(source)

        # Recognise speech using Google Speech Recognition

        try:
            recording.transcript = r.recognize_google(
                audio)  # r.recognize_sphinx(audio)
            recording.save()
        except Exception as e:
            print("Could not request results from Sphinx"
                  " service; {0}".format(e))

        # Delete WAV file.

        os.remove(filename_out)

        #
        # Analyse categories from NLP.
        #
        try:
            if not recording.transcript:
                recording.transcript = "Empty."
            response = settings.TEXTRAZOR_CLIENT.analyze(recording.transcript)

            # Get the top responses.
            count = 0
            categories = []

            for i in response.topics():
                if count < 5:
                    categories.append(i.label)
                else:
                    break

                count += 1

            # Turn into string if there are at least one category.

            if len(categories) == 1:
                categories = categories[0]
            elif len(categories) > 1:
                categories = ", ".join(categories)
            else:
                categories = "Short"
        except Exception as ex:
            print("Failed to analyze with error: " + ex)

            categories = "Short"

        # Finally, save into the DB.

        recording.categories = categories
        recording.save()

        return recording

    class Meta:
        """Meta models, what is shown."""

        model = models.Recording
        fields = ('date', 'transcript', 'clip', 'categories', 'happy',
                  'neutral', 'fear', 'sad', 'angry')


class RecordingViewSet(viewsets.ModelViewSet):
    """Define view behaviour."""

    queryset = models.Recording.objects.all()
    serializer_class = RecordingSerializer


# Determine routing conf.

router = routers.DefaultRouter()
router.register(r'recordings', RecordingViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^test/', views.test)
]


# Show media files if not in debug.

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
