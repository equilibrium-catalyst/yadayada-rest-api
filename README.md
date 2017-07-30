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

This application was not built with security in mind! Do **not** under any circumstances deploy this to a production server!

Documentation
-------------

-	Upload a sound file to the server.

```
HTTP 1.1 POST '/'
'file': some sound file
```

**Not yet implemented. REST-API framework, we need to find out how to actually do the file upload.**

...returns:

```
JSON
'sentiment': an object of strings to integers (out of 100)
'transcript': a long string of the user's speech
'tags': an array of strings
```

-	Query the database given hashtag categories.

```
HTTP 1.1 GET (Authenticated)
'tags': all of the tags that we want to use to rank search
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
