{% from 'django.sls' import virtualenv_path %}

include:
  - django

install-py-dev:
  pkg.installed:
  - name: python-dev

install-libpg:
  pkg.installed:
  - name: libpq-dev

install-psycopg2:
  pip.installed:
  - name: psycopg2
  - bin_env: {{ virtualenv_path }}/bin/pip
  - upgrade: True
  - require:
    - virtualenv: create-virtualenv

{% from 'django.sls' import django_app_path %}
{% from 'django.sls' import db_url %}
#...

run-migrations:
  cmd.run:
  - name: '{{ virtualenv_path }}/bin/python {{ django_app_path }}/manage.py migrate --verbosity 3'
  - env:
    - 'DB_URL': {{ db_url }}
  - require:
    - virtualenv: create-virtualenv
    - pip: install-psycopg2
