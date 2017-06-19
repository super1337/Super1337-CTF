# __SuperLeet CTF__ site made with _Django_

## Instructions

1. Clone the repo: `https://github.com/Ayush21298/SuperLeet-CTF.git`
2. `cd` to the _Django_ project directory: `cd SuperLeet-CTF/webapp-django/`
3. Run the server: `python3 manage.py runserver`

## Troubleshoot

(For Those migrating from python2.x to python3.x)
While running `python3 manage.py runserver` you may get an `import django` error.
The reason being the use of `pip3` instead of `pip`.
Run `pip3 install django` and your problem will be solved.

`OR`

Run `pip3 install -r requirements.txt` in `webapp-django` directory.


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

## Milestones

- [x] Add `django-allauth` to project.
- [x] Add _social logins_ to the project.
- [x] Create core functionalities for the `questionnaire` app.
- [ ] Create scoring system for `questionnaire`.
- [ ] Complete `questionnaire` by making `routes`, `views` and `templates`.
