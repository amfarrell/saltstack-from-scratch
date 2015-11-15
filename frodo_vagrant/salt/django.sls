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
  - name: /vagrant/example-venv
  - requirements: /vagrant/django-example/requirements.txt
  - require:
    - pkg: install-virtualenv
    - git: clone-example-app

gunicorn-upstart-file:
  file.managed:
  - name: /etc/init/django-example.conf
  - source:
    - salt://django-example.conf
    - user: root
    - group: root
    - mode: '0644'

gunicorn-running:
  service.running:
  - name: django-example

