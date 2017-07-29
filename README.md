yadayada-rest-api
=================

Django RESTful backend API for the YadaYada application.

Installation
------------

Just clone the repository, activate the virtualenv, and install the requirements found in `requirements.txt`. After this, cd into the `restapi` directory and:

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
```

Documentation
-------------

-	Upload a sound file to the server.

```
HTTP 1.1 POST
'apikey': some valid API key
'file': some sound file
```

...returns:

```
JSON
'sentiment': an object of strings to integers (out of 100)
'transcript': a long string of the user's speech
'tags': an array of strings
```

-	Query the database given hashtag categories.

```
HTTP 1.1 POST
'apikey': some valid API key
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
