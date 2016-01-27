{% from 'django.sls' import gunicorn_port %}
{% from 'django.sls' import static_root %}
{% from 'django.sls' import static_url %}
{% from 'django.sls' import domain %}

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
  - context:
    gunicorn_port: {{ gunicorn_port }}
    static_root: {{ static_root }}
    static_url: {{ static_url }}
    domain: {{ domain }}
