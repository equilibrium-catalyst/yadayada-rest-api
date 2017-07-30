yadayada-rest-api
=================

Django RESTful backend API for the YadaYada application.

Installation
------------

Get 'ffmpg':

```
$ brew install ffmpeg
```

...or, on Linux:

```
$ sudo apt-get install ffmpeg libavcodec-extra-53
```

Afterwards, just clone the repository, activate the virtualenv, and install the requirements found in `requirements.txt`. After this, cd into the `restapi` directory and:

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
```

Running in debug is easy:

```
$ python manage.py runserver 0:8000 --noreload
```

POST requests must be authenticated. You will need to remember the username:password for the superuser. For instance:

```sh
user: api_user
pass: 7d8bf975-0ec4-430f-95e2-9daf2dbade03
```

WARNING!
--------

This application was not built with security in mind! Do **not** under any circumstances deploy this to a production server, especially one without HTTPS and HSTS enabled.

Hackathon Caveats
-----------------

Because this was made in a hackathon with a time constraint, there are obviously some condsiderations:

-	The file uploaded MUST be a mono mp3.
-	The API cannot handle upload on a slow network.

Documentation
-------------

-	Upload a sound file to the server.

```
HTTP 1.1 POST '/' -a (or --user in CURL) user:password
'clip': some sound file
```

...returns:

```
JSON object
'clip': string, path to clip on the server
'happy': string of decimal, happy emotion
'sad': string of decimal, sadness emotion
'angry': string of decimal, anger emotion
'neutral': string of decimal, neutral emotion
'fear': string of decimal, fearful emotion
'transcript': string, speech-to-text of the recording.
'categories': string, comma separated categories
```

-	Query the database for all recordings sorted by date.

```
HTTP 1.1 GET /recordings?format=json
```

...returns:

```
JSON array of the above JSON objects.
```

CURL examples
-------------

```sh
$ curl -F "clip=@file.mp3" http://endpoint/recordings/ --user uname:password
$ curl http://endpoint/recordings  # This is unauthenticated.
```

Pipeline
--------

When the file is uploaded, it is taken through the following pipeline logic:

1.	File is uploaded and now exists in memory.
2.	File's sentiment (emotions) are analysed and stored in memory in a list.
3.	File is brought through speech-to-text, then through natural language processing to get the context.
4.	File is stored on the file system.
5.	An object is created and placed into the database.
6.	JSON is returned to the user.
