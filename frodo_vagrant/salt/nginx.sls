{% set virtualenv_path = '/vagrant/example-venv' %}
{% set django_app_path = '/vagrant/django-example' %}
{% set django_app_name = 'django_example' %}
{% set gunicorn_service_name = 'django-example' %}

install-nginx:
  pkg.installed:
  - name: nginx

nginx-running:
  service.running:
  - name: nginx
  - watch:
    - file: nginx-conf-file

nginx-conf-file:
  file.managed:
  - name: /etc/nginx/sites-enabled/default
  - source: salt://nginx-default.conf
  - template: jinja
