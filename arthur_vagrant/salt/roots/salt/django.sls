{% set virtualenv_path = '/vagrant/example-venv' %}
{% set django_app_path = '/vagrant/django-example' %}
{% set django_app_name = 'django_example' %}
{% set gunicorn_service_name = 'django-example' %}

install-git:
  pkg.installed:
  - name: git

clone-example-app:
  git.latest:
  - name: https://github.com/amfarrell/django-example
  - target: /vagrant/django-example
  - require:
    - pkg: install-git

install-virtualenv:
  pkg.installed:
  - name: python-virtualenv

create-virtualenv:
  virtualenv.managed:
  - name: {{ virtualenv_path }}
  - requirements: {{ django_app_path }}/requirements.txt
  - require:
    - pkg: install-virtualenv
    - git: clone-example-app

gunicorn-upstart-file:
  file.managed:
  - name: /etc/init/{{ gunicorn_service_name }}.conf
  - source: salt://django-example.conf
  - user: root
  - group: root
  - mode: '0644'
  - template: jinja
  - context:
    django_app_path: {{ django_app_path }}
    virtualenv_path: {{ virtualenv_path }}
    django_app_name: {{ django_app_name }}

gunicorn-running:
  service.running:
  - name: {{ gunicorn_service_name }}
  - require:
    - file: gunicorn-upstart-file
    - virtualenv: create-virtualenv

