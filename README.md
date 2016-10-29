# orator.io
A web-based speech coach that helps users improve their public speaking skills
through analysis of pacing, tone, volume, gestures, and machine learning.

Project progress can be tracked [here](https://potatotank.github.io/oratorio/
"Orator.io Project Page").

### Requirements and installation

Currently only the UW CSE Linux home VM (CentOS) is supported.

Install Python 3.5

TODO

Install Django

TODO

Download the latest release version of from Releases.

Or clone this repository to obtain the latest development version.

### Usage

To run the test suite:

`python manage.py test`

To run a development server on 127.0.0.1:8000:

`python manage.py runserver`

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
