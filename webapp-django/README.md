# __SuperLeet CTF__ site made with _Django_

## Installation

1. Clone the repo: `https://github.com/Ayush21298/SuperLeet-CTF.git`
2. `cd` to the _Django_ project directory: `cd SuperLeet-CTF/webapp-django/`
3. Install _requirements_: `pip3 install -r requirements.txt`
4. _Migrate_ the database: `python3 manage.py migrate`
5. Run the server: `python3 manage.py runserver`

## Troubleshoot

- For Those migrating from `python2.x` to `python3.x`, make sure to install the _requirements_ by following `step 4` of above.

## Project Description

There are 3 [`apps`](https://docs.djangoproject.com/en/1.11/ref/applications/) in this _Django_ `project`.
- _`questionnaire`_: This app will handle the part of the contest consisting of questions (normal or MCQ-type).
- _`jeopadyctf`_: This app will handle the _jeopardy style CTF_ contests.
- _`accounts`_: This app concerns with user profiles.

We're using [_`django-allauth`_](https://www.intenct.nl/projects/django-allauth/) for authentication. _GitHub_, _Google_, and _Facebook_ has been added as '_social login_' providers.
To explore it, visit the routes:
- `http://127.0.0.1:8000/accounts/signup/`
- `http://127.0.0.1:8000/accounts/login/`
- `http://127.0.0.1:8000/accounts/logout/`

### _`addquestions`_ command

There is an `addquestions` command, which adds question from an input `JSON` file to the _database_. This will hopefully make adding new questions a robust process.

Below is an example run of the `addquestions` command.
```
λ python manage.py addquestions
Successfully added questions to DB from 'questionnaire/questions/questions.json'
```

The specifications of this command are below.
```
λ python manage.py addquestions -h
usage: manage.py addquestions [-h] [--version] [-v {0,1,2,3}]
                              [--settings SETTINGS] [--pythonpath PYTHONPATH]
                              [--traceback] [--no-color]
                              [--inputfile INPUTFILE]

Adds the questions from input JSON file to Database.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --inputfile INPUTFILE
                        Path of the input JSON file
```

By default is assumes the input `JSON` file is `questionnaire/questions/questions.json`.

## Milestones

- [x] Add `django-allauth` to project.
- [x] Add _social logins_ to the project.
- [x] Create core functionalities for the `questionnaire` app.
- [ ] Create scoring system for `questionnaire`.
- [ ] Complete `questionnaire` by making `routes`, `views` and `templates`.
- [ ] Make `models` and basic backbone for _jeopardy-style challenges_.
