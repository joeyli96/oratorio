# orator.io
A web-based speech coach that helps users improve their public speaking skills
through analysis of pacing, tone, volume, gestures, and machine learning.

Project progress can be tracked [here](https://potatotank.github.io/oratorio/
"Orator.io Project Page").

### Requirements

Currently only the UW CSE Linux home VM (CentOS) is supported.

This project uses Python 2.7 (pre-installed in the home VM) and Django 1.10.

To install Django

~~~
sudo yum install python-pip
sudo pip install django==1.10
~~~

### Installation

Download the latest release version of oratorio from Releases.

Or clone this repository to obtain the latest development version of oratorio.

### Usage

Firstly, set up your database with

`python manage.py migrate`

Then you can run a development server on 127.0.0.1:8000 with

`python manage.py runserver`

You can also run the test suite with

`python manage.py test`


### Deploy to production

Detailed instructions forthcoming.

### Directory structure

~~~
oratorio/ - Project directory
  manage.py - Django’s admin utility file
  coach/ - Main application directory
    tests/ - Tests for main application
    settings.py - Settings for the main application
    models.py
    views.py
    urls.py
  templates/ - HTML templates for the whole project
  static/ - Images, css and other static files for the whole project
~~~

### Continuous integration setup

Set up Travis CI by following [this](https://travis-ci.org/getting_started)
starter's guide. We set up Travis to run our test suite every time a commit is
pushed, and to notify team members via email and Slack when a test fails.

### Adding a new release version

To release a new version, package the code in a tar file and create a new
release through Github’s Releases feature. Detailed instructions
[here](https://help.github.com/articles/creating-releases/).

### Bug tracking

All bugs and issues should be reported to
https://github.com/PotatoTank/oratorio/issues. Please follow the issue template
and be as informative as possible.
