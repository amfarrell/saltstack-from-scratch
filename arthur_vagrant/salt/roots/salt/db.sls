{% set pg_version = '9.3' %}


install-postgres:
  pkg.installed:
  - name: postgresql-{{ pg_version }}

hba-conf:
  file.managed:
    - name: /etc/postgresql/{{ pg_version }}/main/pg_hba.conf
    - source: salt://pg_hba.conf
    - user: postgres
    - group: postgres
    - mode: 644
    - template: jinja
    - require:
      - pkg: install-postgres
    - context:
      acceptable_hosts: 'foo'

postgres-running:
  service.running:
    - name: postgresql
    - enable: True
    - watch:
      - file: hba-conf

create-pg-user:
  postgres_user.present:
  - name: {{ pillar['database-user'] }}
  - createdb: True
  - encrypted: False
  - superuser: False
  - password: {{ pillar['database-password'] }}
  - login: True
  - db_user: postgres
  - require:
    - file: hba-conf

create-database:
  postgres_database.present:
  - name: {{ pillar['database-name'] }}
  - encoding: 'UTF8'
  - owner: {{ pillar['database-user'] }}
  - db_user: postgres
  - require:
    - postgres_user: create-pg-user
